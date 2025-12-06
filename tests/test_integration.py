"""Integration tests for Labelit."""

import pytest
from pathlib import Path
import tempfile
from labelit.config import Config
from labelit.analyzer import ImageAnalyzer
from labelit.renamer import FileRenamer
from labelit.monitor import FileMonitor


def test_end_to_end_filename_generation():
    """Test complete flow from description to renamed file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        test_file = Path(tmpdir) / "Screenshot 2024-12-05.png"
        test_file.write_text("test content")

        # Simulate getting a description (without AWS)
        analyzer = ImageAnalyzer("us-east-1", "test-model")
        description = "Login Screen with Username Field"

        # Generate filename
        new_filename = analyzer.generate_filename(description, ".png")
        assert new_filename == "login-screen-with-username-field.png"

        # Rename file
        result = FileRenamer.rename_file(str(test_file), new_filename)

        assert result.success is True
        assert result.old_filename == "Screenshot 2024-12-05.png"
        assert result.new_filename == "login-screen-with-username-field.png"
        assert not test_file.exists()
        assert (Path(tmpdir) / new_filename).exists()


def test_end_to_end_with_collision():
    """Test complete flow with filename collision."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_file = Path(tmpdir) / "Screenshot 2024-12-05.png"
        test_file.write_text("test content")

        # Create collision
        collision_file = Path(tmpdir) / "login-screen.png"
        collision_file.write_text("existing content")

        # Process file
        analyzer = ImageAnalyzer("us-east-1", "test-model")
        description = "Login Screen"
        new_filename = analyzer.generate_filename(description, ".png")

        # Rename with collision handling
        result = FileRenamer.rename_file(str(test_file), new_filename)

        assert result.success is True
        assert result.new_filename == "login-screen-2.png"
        assert (Path(tmpdir) / "login-screen-2.png").exists()
        assert collision_file.exists()  # Original file unchanged


def test_screenshot_detection_and_processing():
    """Test screenshot detection logic."""
    # Test Windows patterns
    assert FileMonitor.is_screenshot("Screenshot 2024-12-05.png") is True
    assert FileMonitor.is_screenshot("screenshot_20241205_123456.png") is True

    # Test macOS pattern
    assert FileMonitor.is_screenshot("Screen Shot 2024-12-05.png") is True

    # Test non-screenshots
    assert FileMonitor.is_screenshot("regular-file.png") is False
    assert FileMonitor.is_screenshot("photo.jpg") is False


def test_fallback_filename_generation():
    """Test fallback filename when AWS fails."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.png"
        test_file.touch()

        analyzer = ImageAnalyzer("us-east-1", "test-model")
        fallback = analyzer.get_fallback_filename(str(test_file))

        assert fallback.startswith("image-")
        assert len(fallback) == 21  # image-YYYYMMDD-HHMMSS


def test_config_validation_flow():
    """Test configuration validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        from labelit.config import ConfigManager

        # Create valid config
        config = Config(
            monitored_folder=tmpdir,
            aws_region="us-east-1",
            bedrock_model_id="test-model",
            log_level="INFO",
            process_existing_on_startup=True,
        )

        assert ConfigManager.validate_config(config) is True

        # Test invalid config
        invalid_config = Config(
            monitored_folder="/nonexistent/path",
            aws_region="us-east-1",
            bedrock_model_id="test-model",
            log_level="INFO",
            process_existing_on_startup=True,
        )

        assert ConfigManager.validate_config(invalid_config) is False


def test_multiple_file_processing():
    """Test processing multiple files in sequence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple test files
        files = []
        for i in range(3):
            test_file = Path(tmpdir) / f"Screenshot {i}.png"
            test_file.write_text(f"content {i}")
            files.append(test_file)

        analyzer = ImageAnalyzer("us-east-1", "test-model")

        # Process each file
        descriptions = ["Login Screen", "Settings Menu", "Dashboard View"]
        for i, (file, desc) in enumerate(zip(files, descriptions)):
            new_filename = analyzer.generate_filename(desc, ".png")
            result = FileRenamer.rename_file(str(file), new_filename)

            assert result.success is True
            assert not file.exists()

        # Verify all files were renamed
        renamed_files = list(Path(tmpdir).glob("*.png"))
        assert len(renamed_files) == 3
