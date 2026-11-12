import os
import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "default_config.yaml"

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Loads configuration dictionary from YAML file."""
    path_to_load = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    
    if not path_to_load.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path_to_load}")
        
    with open(path_to_load, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    # Resolve relative paths against workspace root
    workspace_root = DEFAULT_CONFIG_PATH.parent.parent
    if "paths" in config:
        for key, rel_path in config["paths"].items():
            config["paths"][key] = str((workspace_root / rel_path).resolve())
            
    return config
