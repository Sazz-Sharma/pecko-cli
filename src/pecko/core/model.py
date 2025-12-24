from __future__ import annotations

from langchain_openai import ChatOpenAI

from pecko.core.config import load_config
from pecko.core.paths import get_global_config_path, config_path, get_root


def get_model() -> ChatOpenAI:
   
    try:
        root = get_root()
        local_cfg = config_path(root)
    except ValueError:
        local_cfg = None
        
    cfg = load_config(local_path=local_cfg, global_path=get_global_config_path())
    
    profile = cfg.profiles.get(cfg.active_profile)
    if not profile:
        raise ValueError(f"Active profile '{cfg.active_profile}' not found in config.")

    return ChatOpenAI(
        model=profile.model,
        api_key=profile.api_key,
        base_url=profile.base_url,
        temperature=0
    )