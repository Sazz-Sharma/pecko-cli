from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from pecko.core.paths import find_repo_root, pecko_dir, PECKO_DIRNAME, config_path, get_global_config_path
from pecko.core.config import PeckoConfig, write_config, read_config, load_config


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
) -> None:
    """
    Configure pecko settings.
    """
    if global_config and local_config:
        console.print("[red]Error: Cannot specify both --global and --local[/red]")
        raise typer.Exit(1)

    if not global_config and not local_config:
        # Default behavior: show current effective config
        root = find_repo_root(Path.cwd())
        local_cfg_path = config_path(root) if root else None
        global_cfg_path = get_global_config_path()
        
        cfg = load_config(local_path=local_cfg_path, global_path=global_cfg_path)
        console.print(Panel.fit(str(cfg), title="Effective Configuration"))
        return

    target_path: Path
    if global_config:
        target_path = get_global_config_path()
        title = "Global Configuration"
    else:
        # Local config requires being in a repo
        root = find_repo_root(Path.cwd())
        if not root:
            console.print("[red]Error: Not inside a pecko workspace. Run 'pecko init' first or use --global.[/red]")
            raise typer.Exit(1)
        target_path = config_path(root)
        title = "Local Configuration"

    # Load existing or default
    current_cfg = read_config(target_path) if target_path.exists() else PeckoConfig()
    
    console.print(f"[bold]{title}[/bold]")
    
    new_model = Prompt.ask("Default Model", default=current_cfg.default_model)
    
    # Update config
    current_cfg.default_model = new_model
    
    # Save
    write_config(target_path, current_cfg)
    console.print(f"[green]Configuration saved to {target_path}[/green]")


def main():
    app()


if __name__ == "__main__":
    main()
