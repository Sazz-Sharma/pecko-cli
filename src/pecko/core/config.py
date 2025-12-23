from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PeckoConfig:
    version: int = 1
    default_model: str = "gpt-4o"
    created_by: str = "pecko"


def load_config(local_path: Path | None = None, global_path: Path | None = None) -> PeckoConfig:
    """
    Load configuration with priority: local > global > default.
    """
    # Start with defaults
    cfg = PeckoConfig()

    # Load global if exists
    if global_path and global_path.exists():
        try:
            global_cfg = read_config(global_path)
            # Update fields from global
            for k, v in asdict(global_cfg).items():
                if hasattr(cfg, k):
                    setattr(cfg, k, v)
        except Exception:
            pass  # Ignore errors in global config for now

    # Load local if exists (overrides global)
    if local_path and local_path.exists():
        try:
            local_cfg = read_config(local_path)
            for k, v in asdict(local_cfg).items():
                if hasattr(cfg, k):
                    setattr(cfg, k, v)
        except Exception:
            pass

    return cfg


def write_config(path: Path, cfg: PeckoConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(cfg), indent=2) + "\n", encoding="utf-8")


def read_config(path: Path) -> PeckoConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    return PeckoConfig(**data)
