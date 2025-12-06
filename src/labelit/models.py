"""Data models for Labelit."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RenameResult:
    """Result of a file rename operation."""

    success: bool
    old_path: str
    new_path: str
    old_filename: str
    new_filename: str
    timestamp: datetime
    error_message: Optional[str] = None


@dataclass
class ProcessingStats:
    """Statistics for file processing operations."""

    total_processed: int = 0
    successful: int = 0
    failed: int = 0
    start_time: Optional[datetime] = None
