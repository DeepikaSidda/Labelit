"""Tests for image analyzer."""

import pytest
from labelit.analyzer import ImageAnalyzer


def test_sanitize_filename_basic():
    """Test basic filename sanitization."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.sanitize_filename("Login Screen with Username Field")
    assert result == "login-screen-with-username-field"


def test_sanitize_filename_special_characters():
    """Test sanitization removes special characters."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.sanitize_filename("Code Editor! (Dark Mode)")
    assert result == "code-editor-dark-mode"


def test_sanitize_filename_length_limit():
    """Test filename length is limited to 50 characters."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    long_text = "This is a very long description that exceeds fifty characters"
    result = analyzer.sanitize_filename(long_text)
    assert len(result) <= 50


def test_sanitize_filename_lowercase():
    """Test all characters are converted to lowercase."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.sanitize_filename("UPPERCASE TEXT")
    assert result == "uppercase-text"
    assert result.islower() or "-" in result


def test_sanitize_filename_spaces_to_hyphens():
    """Test spaces are replaced with hyphens."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.sanitize_filename("multiple   spaces   here")
    assert "  " not in result
    assert result == "multiple-spaces-here"


def test_sanitize_filename_first_sentence():
    """Test only first sentence is used."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.sanitize_filename("First sentence. Second sentence.")
    assert "second" not in result
    assert result == "first-sentence"


def test_sanitize_filename_removes_leading_trailing_hyphens():
    """Test leading and trailing hyphens are removed."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.sanitize_filename("---test---")
    assert not result.startswith("-")
    assert not result.endswith("-")
    assert result == "test"


def test_generate_filename():
    """Test filename generation with extension."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    result = analyzer.generate_filename("Test Description", ".png")
    assert result == "test-description.png"
    assert result.endswith(".png")


def test_get_fallback_filename(tmp_path):
    """Test fallback filename generation."""
    analyzer = ImageAnalyzer("us-east-1", "test-model")
    test_file = tmp_path / "test.png"
    test_file.touch()

    result = analyzer.get_fallback_filename(str(test_file))
    assert result.startswith("image-")
    assert len(result) == 21  # image-YYYYMMDD-HHMMSS
