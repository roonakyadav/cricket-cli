"""Configuration module for cricket CLI"""

import os
import json
from typing import Dict, Any

CONFIG_FILE_PATH = os.path.expanduser("~/.cricket_config.json")

DEFAULT_CONFIG = {
    "refresh_interval": 30,
    "default_filter": "",
    "timeout": 10,
    "headers": {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Cricket-CLI/1.1.0"
    },
    "sources": {
        "cricbuzz_enabled": True,
        "espn_enabled": True
    }
}


def load_config() -> Dict[str, Any]:
    """Load configuration from file, create default if doesn't exist"""
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except (json.JSONDecodeError, IOError):
            # If config file is corrupted, return defaults
            return DEFAULT_CONFIG
    else:
        # Create default config file
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Warning: Could not save config file: {e}")


def get_config_value(key: str, default=None):
    """Get a specific configuration value"""
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """Set a specific configuration value"""
    config = load_config()
    config[key] = value
    save_config(config)