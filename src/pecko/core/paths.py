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
