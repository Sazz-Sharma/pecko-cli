from __future__ import annotations

from pathlib import Path


PECKO_DIRNAME = ".pecko"
CONFIG_FILENAME = "config.json"


def find_repo_root(start: Path) -> Path | None:

    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / PECKO_DIRNAME).is_dir():
            return p
    return None


def pecko_dir(root: Path) -> Path:
    return root / PECKO_DIRNAME


def config_path(root: Path) -> Path:
    return pecko_dir(root) / CONFIG_FILENAME


def get_root() -> Path:
    """Helper to get the repo root or raise error if not in a pecko repo."""
    root = find_repo_root(Path.cwd())
    if not root:
        raise ValueError("Not inside a pecko-initialized workspace.")
    return root


def safe_path(path_str: str) -> Path:
    """
    Resolve path relative to repo root and ensure it doesn't escape the root.
    """
    root = get_root()
    # Treat path as relative to root
    target = (root / path_str).resolve()

    # Security check: ensure target is inside root
    if not str(target).startswith(str(root)):
        raise ValueError(f"Access denied: {path_str} is outside the workspace root.")

    return target


