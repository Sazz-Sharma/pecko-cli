from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PeckoConfig:
    version: int = 1
    default_model: str = "gpt-4o"
    created_by: str = "pecko"


def write_config(path: Path, cfg: PeckoConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(cfg), indent=2) + "\n", encoding="utf-8")


def read_config(path: Path) -> PeckoConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    return PeckoConfig(**data)
