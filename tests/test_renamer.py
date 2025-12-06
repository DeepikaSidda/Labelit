"""Tests for file renamer."""

import pytest
from pathlib import Path
import tempfile
from labelit.renamer import FileRenamer


def test_check_collision_no_collision(tmp_path):
    """Test collision check when file doesn't exist."""
    result = FileRenamer.check_collision(str(tmp_path), "nonexistent.png")
    assert result is False


def test_check_collision_with_collision(tmp_path):
    """Test collision check when file exists."""
    test_file = tmp_path / "existing.png"
    test_file.touch()

    result = FileRenamer.check_collision(str(tmp_path), "existing.png")
    assert result is True


def test_resolve_collision_no_collision(tmp_path):
    """Test resolve collision when no collision exists."""
    result = FileRenamer.resolve_collision(str(tmp_path), "test.png")
    assert result == "test.png"


def test_resolve_collision_with_collision(tmp_path):
    """Test resolve collision appends -2 suffix."""
    test_file = tmp_path / "test.png"
    test_file.touch()

    result = FileRenamer.resolve_collision(str(tmp_path), "test.png")
    assert result == "test-2.png"


def test_resolve_collision_multiple_collisions(tmp_path):
    """Test resolve collision increments suffix."""
    (tmp_path / "test.png").touch()
    (tmp_path / "test-2.png").touch()
    (tmp_path / "test-3.png").touch()

    result = FileRenamer.resolve_collision(str(tmp_path), "test.png")
    assert result == "test-4.png"


def test_rename_file_success(tmp_path):
    """Test successful file rename."""
    old_file = tmp_path / "old.png"
    old_file.write_text("test content")

    result = FileRenamer.rename_file(str(old_file), "new.png")

    assert result.success is True
    assert result.old_filename == "old.png"
    assert result.new_filename == "new.png"
    assert not old_file.exists()
    assert (tmp_path / "new.png").exists()


def test_rename_file_with_collision(tmp_path):
    """Test rename with collision handling."""
    old_file = tmp_path / "old.png"
    old_file.write_text("test content")

    # Create collision
    (tmp_path / "new.png").touch()

    result = FileRenamer.rename_file(str(old_file), "new.png")

    assert result.success is True
    assert result.new_filename == "new-2.png"
    assert (tmp_path / "new-2.png").exists()


def test_rename_file_preserves_extension(tmp_path):
    """Test that file extension is preserved."""
    old_file = tmp_path / "test.jpg"
    old_file.touch()

    result = FileRenamer.rename_file(str(old_file), "renamed.jpg")

    assert result.success is True
    assert result.new_filename.endswith(".jpg")
