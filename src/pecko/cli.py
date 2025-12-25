from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from pecko.core.paths import find_repo_root, pecko_dir, PECKO_DIRNAME, config_path, get_global_config_path
from pecko.core.config import PeckoConfig, write_config, read_config, load_config, LLMProfile
from pecko.workflow.graph import create_graph
from langchain_core.messages import HumanMessage


app = typer.Typer(help="pecko — local repo CLI")
console = Console()


def init_repo(root: Path, *, force: bool = False) -> tuple[bool, str]:
    """
    Initialize a pecko workspace in 'root'.

    Returns (created, message)
    """
    root = root.resolve()
    pd = pecko_dir(root)
    cfg_path = config_path(root)

    if pd.exists() and not force:
        return (False, f"Already initialized: {root}")

    pd.mkdir(parents=True, exist_ok=True)

    # config
    write_config(cfg_path, PeckoConfig())

    marker = pd / "README.txt"
    marker.write_text(
        "This folder is managed by pecko.\n"
        "It stores workspace config and agent state.\n",
        encoding="utf-8",
    )

    return (True, f"Initialized pecko workspace in: {root}")

@app.command()
def init(
    path: Path = typer.Argument(Path("."), help="Directory to initialize"),
    force: bool = typer.Option(False, "--force", help="Re-initialize if already initialized"),
) -> None:
    """
    Initialize a pecko workspace in PATH by creating .pecko/ and config.json.
    """
    created, msg = init_repo(path, force=force)
    style = "green" if created else "yellow"
    console.print(Panel.fit(msg, style=style))


@app.command()
def status(
    path: Path = typer.Argument(Path("."), help="Directory to check"),
) -> None:
    """
    Show whether PATH is inside a pecko-initialized workspace.
    """
    root = find_repo_root(path)
    if not root:
        console.print("[red]Not initialized.[/red] Run: pecko init")
        raise typer.Exit(1)

    console.print(Panel.fit(f"[bold]Initialized[/bold]\nroot: {root}\nmeta: {pecko_dir(root)}"))


@app.command()
def config(
    global_config: bool = typer.Option(False, "--global", help="Configure global settings"),
    local_config: bool = typer.Option(False, "--local", help="Configure local settings"),
    list_profiles: bool = typer.Option(False, "--list", help="List all available profiles"),
    set_active: str = typer.Option(None, "--set-active", help="Set the active profile"),
    copy_global: bool = typer.Option(False, "--copy-global", help="Copy global configuration to local"),
) -> None:
    """
    Configure pecko settings.
    """
    if global_config and local_config:
        console.print("[red]Error: Cannot specify both --global and --local[/red]")
        raise typer.Exit(1)

   
    if copy_global:
        root = find_repo_root(Path.cwd())
        if not root:
            console.print("[red]Error: Not inside a pecko workspace. Run 'pecko init' first.[/red]")
            raise typer.Exit(1)

        global_path = get_global_config_path()
        if not global_path.exists():
            console.print("[red]Error: No global configuration found.[/red]")
            raise typer.Exit(1)

        local_path = config_path(root)
        global_cfg = read_config(global_path)

        if local_path.exists():
            local_cfg = read_config(local_path)
        else:
            local_cfg = PeckoConfig()

      
        local_cfg.profiles.update(global_cfg.profiles)
        local_cfg.active_profile = global_cfg.active_profile

        write_config(local_path, local_cfg)
        console.print(f"[green]Successfully copied global configuration to local: {local_path}[/green]")
        return


    target_path: Path | None = None
    title = "Effective Configuration"
    
    if global_config:
        target_path = get_global_config_path()
        title = "Global Configuration"
    elif local_config:
        root = find_repo_root(Path.cwd())
        if not root:
            console.print("[red]Error: Not inside a pecko workspace. Run 'pecko init' first or use --global.[/red]")
            raise typer.Exit(1)
        target_path = config_path(root)
        title = "Local Configuration"
    else:
        # Default to local if in repo, else global
        root = find_repo_root(Path.cwd())
        if root:
            target_path = config_path(root)
            title = "Local Configuration (Default)"
        else:
            target_path = get_global_config_path()
            title = "Global Configuration (Default)"

    if target_path and target_path.exists():
        current_cfg = read_config(target_path)
    else:
        current_cfg = PeckoConfig()

    # --list
    if list_profiles:
        console.print(f"[bold]{title}[/bold]")
        for name, profile in current_cfg.profiles.items():
            is_active = (name == current_cfg.active_profile)
            style = "green bold" if is_active else "white"
            prefix = "* " if is_active else "  "
            console.print(f"[{style}]{prefix}{name}[/{style}] - {profile.provider}/{profile.model}")
        return

    # --set-active
    if set_active:
        if set_active not in current_cfg.profiles:
            console.print(f"[red]Error: Profile '{set_active}' not found.[/red]")
            raise typer.Exit(1)
        current_cfg.active_profile = set_active
        if target_path:
            write_config(target_path, current_cfg)
            console.print(f"[green]Active profile set to '{set_active}' in {title}[/green]")
        return

    if not global_config and not local_config:
        root = find_repo_root(Path.cwd())
        local_cfg_path = config_path(root) if root else None
        global_cfg_path = get_global_config_path()
        
        cfg = load_config(local_path=local_cfg_path, global_path=global_cfg_path)
        console.print(Panel.fit(str(cfg), title="Effective Configuration"))
        return

    
    console.print(f"[bold]{title}[/bold]")
    
    
    profile_name = Prompt.ask("Profile Name", default=current_cfg.active_profile)
    
   
    if profile_name in current_cfg.profiles:
        profile = current_cfg.profiles[profile_name]
        console.print(f"[blue]Editing existing profile: {profile_name}[/blue]")
    else:
        console.print(f"[green]Creating new profile: {profile_name}[/green]")
        profile = LLMProfile(name=profile_name)

    
    profile.provider = Prompt.ask("Provider", default=profile.provider, choices=["openai", "anthropic", "ollama", "other"])
    profile.model = Prompt.ask("Model Name", default=profile.model)
    profile.base_url = Prompt.ask("Base URL (optional)", default=profile.base_url or "")
    if profile.base_url == "": profile.base_url = None
    
    profile.api_key = Prompt.ask("API Key (optional, leave empty to use env vars)", default=profile.api_key or "", password=True)
    if profile.api_key == "": profile.api_key = None

 
    current_cfg.profiles[profile_name] = profile
    current_cfg.active_profile = profile_name
    
    if target_path:
        write_config(target_path, current_cfg)
        console.print(f"[green]Configuration saved to {target_path}[/green]")
        console.print(f"Active Profile: [bold]{profile_name}[/bold]")


@app.command()
def run(
    prompt: str = typer.Argument(..., help="The instruction for the agent"),
) -> None:
    """
    Run the Pecko agent with a prompt.
    """
  
    root = find_repo_root(Path.cwd())
    if not root:
        console.print("[red]Error: Not inside a pecko workspace. Run 'pecko init' first.[/red]")
        raise typer.Exit(1)

    console.print(f"[bold blue]Pecko Agent Running...[/bold blue]")
    console.print(f"Task: {prompt}")

    try:
        graph = create_graph()
        
       
        inputs = {"messages": [HumanMessage(content=prompt)]}
        
        
        for chunk in graph.stream(inputs, stream_mode="values"):
            
            messages = chunk.get("messages", [])
            
            if messages:
                last_msg = messages[-1]
                
                if last_msg.type == "ai":
                    console.print(Panel(last_msg.content, title="Agent", border_style="blue"))
                elif last_msg.type == "tool":
                    console.print(f"[dim]Tool Output: {last_msg.name}[/dim]")

    except Exception as e:
        console.print(f"[red]Agent Error: {e}[/red]")
        raise typer.Exit(1)


def main():
    app()


if __name__ == "__main__":
    main()
