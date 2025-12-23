from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, Any


@dataclass
class LLMProfile:
    name: str
    provider: str = "openai"
    model: str = "gpt-4o"
    base_url: str | None = None
    api_key: str | None = None


@dataclass
class PeckoConfig:
    version: int = 1
    active_profile: str = "default"
    profiles: Dict[str, LLMProfile] = field(default_factory=lambda: {
        "default": LLMProfile(name="default", provider="openai", model="gpt-4o")
    })
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
            cfg.active_profile = global_cfg.active_profile
            # Merge profiles
            cfg.profiles.update(global_cfg.profiles)
        except Exception:
            pass  # Ignore errors in global config for now

    # Load local if exists (overrides global)
    if local_path and local_path.exists():
        try:
            local_cfg = read_config(local_path)
            cfg.active_profile = local_cfg.active_profile
            # Merge profiles (local overrides global with same name)
            cfg.profiles.update(local_cfg.profiles)
        except Exception:
            pass

    return cfg


def write_config(path: Path, cfg: PeckoConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(cfg), indent=2) + "\n", encoding="utf-8")


def read_config(path: Path) -> PeckoConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    
    # Migration: Handle old config with 'default_model'
    if "default_model" in data:
        old_model = data.pop("default_model")
        if "profiles" not in data:
            data["profiles"] = {
                "default": {
                    "name": "default",
                    "provider": "openai",
                    "model": old_model
                }
            }
        if "active_profile" not in data:
            data["active_profile"] = "default"

    # Reconstruct LLMProfile objects
    if "profiles" in data:
        profiles = {}
        for k, v in data["profiles"].items():
            profiles[k] = LLMProfile(**v)
        data["profiles"] = profiles
        
    return PeckoConfig(**data)
