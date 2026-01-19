"""Cache module for cricket CLI"""

import json
import os
import time
from typing import Any, Dict, Optional

CACHE_FILE_PATH = os.path.expanduser("~/.cricket_cache.json")
CACHE_DURATION = 60 * 2  # Cache duration in seconds (2 minutes)
CACHE_DIR = os.path.expanduser("~/.cricket")  # Directory for cache files


def load_cache() -> Dict[str, Any]:
    """Load cache from file, return empty dict if doesn't exist or expired"""
    if not os.path.exists(CACHE_FILE_PATH):
        return {}
    
    try:
        with open(CACHE_FILE_PATH, 'r') as f:
            cached_data = json.load(f)
        
        # Check if cache is expired
        current_time = time.time()
        if current_time - cached_data.get("timestamp", 0) > CACHE_DURATION:
            # Cache expired, return empty dict
            return {}
        
        return cached_data
    except (json.JSONDecodeError, IOError):
        # If cache file is corrupted, return empty dict
        return {}


def save_cache(data: Any) -> None:
    """Save data to cache file"""
    cache_data = {
        "data": data,
        "timestamp": time.time()
    }
    
    try:
        with open(CACHE_FILE_PATH, 'w') as f:
            json.dump(cache_data, f)
    except IOError as e:
        print(f"Warning: Could not save cache: {e}")


def get_cached_matches() -> Optional[Any]:
    """Get cached matches if available and not expired"""
    cached_data = load_cache()
    return cached_data.get("data") if cached_data else None


def cache_matches(matches: Any) -> None:
    """Cache matches data"""
    save_cache(matches)


def is_cache_valid() -> bool:
    """Check if cache exists and is still valid"""
    cached_data = load_cache()
    return bool(cached_data)