"""Main Labelit service orchestration."""

import logging
import signal
import sys
from pathlib import Path
from typing import Optional
from .config import Config
from .monitor import FileMonitor
from .analyzer import ImageAnalyzer
from .renamer import FileRenamer
from .models import ProcessingStats
from datetime import datetime


class LabelitService:
    """Main service that orchestrates all components."""

    def __init__(self, config: Config):
        """
        Initialize the Labelit service.

        Args:
            config: Configuration object
        """
        self.config = config
        self.monitor: Optional[FileMonitor] = None
        self.analyzer: Optional[ImageAnalyzer] = None
        self.renamer = FileRenamer()
        self.stats = ProcessingStats()
        self.logger = logging.getLogger(__name__)
        self._running = False

    def start(self) -> None:
        """Start the Labelit service."""
        self.logger.info("Starting Labelit service...")

        # Initialize components
        self.analyzer = ImageAnalyzer(self.config.aws_region, self.config.bedrock_model_id)
        self.monitor = FileMonitor(self.config.monitored_folder, self.process_file)

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        # Process existing files if configured
        if self.config.process_existing_on_startup:
            self.logger.info("Processing existing files...")
            self.process_existing_files()

        # Start monitoring
        self.logger.info(f"Monitoring folder: {self.config.monitored_folder}")
        self.monitor.start()
        self._running = True

        # Keep the service running
        try:
            while self._running:
                signal.pause()
        except AttributeError:
            # signal.pause() not available on Windows
            import time

            while self._running:
                time.sleep(1)

    def stop(self) -> None:
        """Stop the Labelit service."""
        self.logger.info("Stopping Labelit service...")
        self._running = False

        if self.monitor:
            self.monitor.stop()

        self.logger.info(
            f"Service stopped. Processed: {self.stats.total_processed}, "
            f"Successful: {self.stats.successful}, Failed: {self.stats.failed}"
        )

    def process_file(self, file_path: str) -> None:
        """
        Process a single file.

        Args:
            file_path: Path to the file to process
        """
        self.logger.info(f"Processing file: {file_path}")
        self.stats.total_processed += 1

        try:
            # Analyze image
            description = self.analyzer.analyze_image(file_path)
            self.logger.debug(f"Got description: {description}")

            # Generate filename
            original_ext = Path(file_path).suffix
            new_filename = self.analyzer.generate_filename(description, original_ext)
            self.logger.debug(f"Generated filename: {new_filename}")

            # Rename file
            result = self.renamer.rename_file(file_path, new_filename)

            if result.success:
                self.stats.successful += 1
                self.logger.info(
                    f"Successfully renamed: {result.old_filename} -> {result.new_filename}"
                )
            else:
                self.stats.failed += 1
                self.logger.error(
                    f"Failed to rename {result.old_filename}: {result.error_message}"
                )

        except Exception as e:
            self.stats.failed += 1
            self.logger.error(f"Error processing {file_path}: {str(e)}", exc_info=True)

    def process_existing_files(self) -> None:
        """Process all existing screenshot files in the monitored folder."""
        folder = Path(self.config.monitored_folder)

        if not folder.exists():
            self.logger.warning(f"Monitored folder does not exist: {folder}")
            return

        # Get screenshot patterns
        patterns = FileMonitor.get_screenshot_patterns()

        # Find all matching files
        matching_files = []
        for file_path in folder.iterdir():
            if file_path.is_file() and FileMonitor.is_screenshot(file_path.name):
                matching_files.append(str(file_path))

        self.logger.info(f"Found {len(matching_files)} existing screenshot files")

        # Process each file
        for file_path in matching_files:
            self.process_file(file_path)

    def handle_shutdown(self, signum, frame) -> None:
        """
        Handle shutdown signals.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
