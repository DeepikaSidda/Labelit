"""
Labelit - Automatic screenshot renaming using AWS Bedrock AI.

A lightweight Python background service that monitors folders for new screenshots
and automatically renames them with descriptive names using AWS Bedrock's multimodal AI.
"""

__version__ = "0.1.0"
__author__ = "Labelit Contributors"
__license__ = "MIT"

from .config import Config, ConfigManager
from .models import RenameResult, ProcessingStats

__all__ = [
    "Config",
    "ConfigManager",
    "RenameResult",
    "ProcessingStats",
]
