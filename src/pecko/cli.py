from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from pecko.core.paths import find_repo_root, pecko_dir, PECKO_DIRNAME, config_path
from pecko.core.config import PeckoConfig, write_config


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


def main():
    app()


if __name__ == "__main__":
    main()
