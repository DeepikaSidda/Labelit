"""File renaming with collision handling."""

import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional
from .models import RenameResult


class FileRenamer:
    """Handles file renaming operations with collision detection."""

    @staticmethod
    def rename_file(old_path: str, new_name: str) -> RenameResult:
        """
        Rename a file with collision handling.

        Args:
            old_path: Current path to the file
            new_name: New filename (without path)

        Returns:
            RenameResult with operation details
        """
        old_path_obj = Path(old_path)
        directory = old_path_obj.parent
        old_filename = old_path_obj.name

        # Resolve any collisions
        final_name = FileRenamer.resolve_collision(str(directory), new_name)
        new_path = directory / final_name

        try:
            # Perform the rename
            old_path_obj.rename(new_path)

            return RenameResult(
                success=True,
                old_path=old_path,
                new_path=str(new_path),
                old_filename=old_filename,
                new_filename=final_name,
                timestamp=datetime.now(),
            )

        except Exception as e:
            return RenameResult(
                success=False,
                old_path=old_path,
                new_path=str(new_path),
                old_filename=old_filename,
                new_filename=final_name,
                timestamp=datetime.now(),
                error_message=str(e),
            )

    @staticmethod
    def check_collision(directory: str, filename: str) -> bool:
        """
        Check if a filename already exists in the directory.

        Args:
            directory: Directory path
            filename: Filename to check

        Returns:
            True if the file exists
        """
        target_path = Path(directory) / filename

        # OS-specific case sensitivity
        system = platform.system()

        if system in ["Windows", "Darwin"]:  # Case-insensitive
            # Check if any file with case-insensitive match exists
            if target_path.exists():
                return True

            # Also check for case variations
            parent = Path(directory)
            if parent.exists():
                for existing_file in parent.iterdir():
                    if existing_file.name.lower() == filename.lower():
                        return True

            return False
        else:  # Linux - case-sensitive
            return target_path.exists()

    @staticmethod
    def resolve_collision(directory: str, filename: str) -> str:
        """
        Resolve filename collisions by appending numeric suffixes.

        Args:
            directory: Directory path
            filename: Desired filename

        Returns:
            Unique filename with suffix if needed
        """
        if not FileRenamer.check_collision(directory, filename):
            return filename

        # Split filename and extension
        path = Path(filename)
        name_without_ext = path.stem
        extension = path.suffix

        # Try incrementing suffixes starting from 2
        counter = 2
        while True:
            new_filename = f"{name_without_ext}-{counter}{extension}"
            if not FileRenamer.check_collision(directory, new_filename):
                return new_filename
            counter += 1

            # Safety check to prevent infinite loop
            if counter > 1000:
                # Use timestamp as last resort
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                return f"{name_without_ext}-{timestamp}{extension}"
