"""Tests for file monitor."""

import pytest
import platform
from labelit.monitor import FileMonitor


def test_get_screenshot_patterns_windows(monkeypatch):
    """Test screenshot patterns for Windows."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    patterns = FileMonitor.get_screenshot_patterns()
    assert "Screenshot*.png" in patterns
    assert "screenshot_*.png" in patterns


def test_get_screenshot_patterns_macos(monkeypatch):
    """Test screenshot patterns for macOS."""
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    patterns = FileMonitor.get_screenshot_patterns()
    assert "Screen Shot*.png" in patterns


def test_get_screenshot_patterns_linux(monkeypatch):
    """Test screenshot patterns for Linux."""
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    patterns = FileMonitor.get_screenshot_patterns()
    assert "Screenshot*.png" in patterns


def test_is_screenshot_windows_pattern():
    """Test screenshot detection for Windows pattern."""
    assert FileMonitor.is_screenshot("Screenshot 2024-12-05.png") is True
    assert FileMonitor.is_screenshot("screenshot_20241205.png") is True


def test_is_screenshot_macos_pattern():
    """Test screenshot detection for macOS pattern."""
    assert FileMonitor.is_screenshot("Screen Shot 2024-12-05.png") is True


def test_is_screenshot_not_matching():
    """Test non-screenshot files are not detected."""
    assert FileMonitor.is_screenshot("regular-file.png") is False
    assert FileMonitor.is_screenshot("photo.jpg") is False
    assert FileMonitor.is_screenshot("document.pdf") is False


def test_is_screenshot_case_sensitive():
    """Test screenshot detection is case-sensitive."""
    assert FileMonitor.is_screenshot("screenshot 2024.png") is False  # lowercase 's'
    assert FileMonitor.is_screenshot("SCREENSHOT 2024.png") is False  # uppercase
