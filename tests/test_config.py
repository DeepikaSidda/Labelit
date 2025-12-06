"""Tests for configuration management."""

import pytest
from pathlib import Path
import tempfile
import os
from labelit.config import Config, ConfigManager


def test_config_dataclass():
    """Test Config dataclass creation."""
    config = Config(
        monitored_folder="/test/path",
        aws_region="us-west-2",
        bedrock_model_id="test-model",
        log_level="DEBUG",
        process_existing_on_startup=False,
    )
    assert config.monitored_folder == "/test/path"
    assert config.aws_region == "us-west-2"
    assert config.bedrock_model_id == "test-model"
    assert config.log_level == "DEBUG"
    assert config.process_existing_on_startup is False


def test_create_default_config():
    """Test creating default configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = ConfigManager.create_default_config(config_path)

        assert config_path.exists()
        assert config.aws_region == "us-east-1"
        assert config.log_level == "INFO"
        assert config.process_existing_on_startup is True


def test_load_config_creates_default_if_missing():
    """Test that load_config creates default if file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        config = ConfigManager.load_config(config_path)

        assert config_path.exists()
        assert isinstance(config, Config)


def test_validate_config_with_valid_folder():
    """Test config validation with valid folder."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            monitored_folder=tmpdir,
            aws_region="us-east-1",
            bedrock_model_id="test-model",
            log_level="INFO",
            process_existing_on_startup=True,
        )
        assert ConfigManager.validate_config(config) is True


def test_validate_config_with_invalid_folder():
    """Test config validation with non-existent folder."""
    config = Config(
        monitored_folder="/nonexistent/path",
        aws_region="us-east-1",
        bedrock_model_id="test-model",
        log_level="INFO",
        process_existing_on_startup=True,
    )
    assert ConfigManager.validate_config(config) is False


def test_validate_config_with_invalid_log_level():
    """Test config validation with invalid log level."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            monitored_folder=tmpdir,
            aws_region="us-east-1",
            bedrock_model_id="test-model",
            log_level="INVALID",
            process_existing_on_startup=True,
        )
        assert ConfigManager.validate_config(config) is False
