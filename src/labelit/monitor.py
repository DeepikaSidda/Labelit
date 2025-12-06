"""File monitoring for screenshot detection."""

import os
import platform
from pathlib import Path
from typing import Callable, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent


class FileMonitor:
    """Monitors a folder for new screenshot files."""

    def __init__(self, folder_path: str, callback: Callable[[str], None]):
        """
        Initialize the file monitor.

        Args:
            folder_path: Path to the folder to monitor
            callback: Function to call when a screenshot is detected
        """
        self.folder_path = folder_path
        self.callback = callback
        self.observer = None
        self._handler = None

    def start(self) -> None:
        """Start monitoring the folder."""
        self._handler = ScreenshotHandler(self.callback, self.get_screenshot_patterns())
        self.observer = Observer()
        self.observer.schedule(self._handler, self.folder_path, recursive=False)
        self.observer.start()

    def stop(self) -> None:
        """Stop monitoring the folder."""
        if self.observer:
            self.observer.stop()
            self.observer.join()

    @staticmethod
    def get_screenshot_patterns() -> List[str]:
        """Get OS-specific screenshot filename patterns."""
        system = platform.system()

        if system == "Windows":
            return ["Screenshot*.png", "screenshot_*.png"]
        elif system == "Darwin":  # macOS
            return ["Screen Shot*.png"]
        else:  # Linux and others
            return ["Screenshot*.png"]

    @staticmethod
    def is_screenshot(filename: str) -> bool:
        """
        Check if a filename matches screenshot patterns.

        Args:
            filename: The filename to check

        Returns:
            True if the filename matches a screenshot pattern
        """
        # Check for Windows patterns
        if filename.startswith("Screenshot") and filename.endswith(".png"):
            return True
        if filename.startswith("screenshot_") and filename.endswith(".png"):
            return True

        # Check for macOS pattern
        if filename.startswith("Screen Shot") and filename.endswith(".png"):
            return True

        return False


class ScreenshotHandler(FileSystemEventHandler):
    """Handles file system events for screenshot detection."""

    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

    def __init__(self, callback: Callable[[str], None], patterns: List[str]):
        """
        Initialize the handler.

        Args:
            callback: Function to call when a screenshot is detected
            patterns: List of filename patterns to match
        """
        super().__init__()
        self.callback = callback
        self.patterns = patterns

    def on_created(self, event: FileCreatedEvent) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = event.src_path
        filename = Path(file_path).name
        extension = Path(file_path).suffix.lower()

        # Check if it's an image file
        if extension not in self.SUPPORTED_EXTENSIONS:
            return

        # Check if it matches screenshot patterns
        if FileMonitor.is_screenshot(filename):
            # Add small delay to ensure file is fully written
            import time
            time.sleep(0.5)
            self.callback(file_path)
