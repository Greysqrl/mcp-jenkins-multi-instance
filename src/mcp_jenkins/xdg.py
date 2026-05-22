"""XDG Base Directory Specification utilities."""

import os
from pathlib import Path


def get_config_dir() -> Path:
    """Get XDG config directory for mcp-jenkins."""
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        return Path(xdg_config_home) / "mcp-jenkins"
    return Path.home() / ".config" / "mcp-jenkins"


def get_data_dir() -> Path:
    """Get XDG data directory for mcp-jenkins."""
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "mcp-jenkins"
    return Path.home() / ".local" / "share" / "mcp-jenkins"


def get_cache_dir() -> Path:
    """Get XDG cache directory for mcp-jenkins."""
    xdg_cache_home = os.environ.get("XDG_CACHE_HOME")
    if xdg_cache_home:
        return Path(xdg_cache_home) / "mcp-jenkins"
    return Path.home() / ".cache" / "mcp-jenkins"
