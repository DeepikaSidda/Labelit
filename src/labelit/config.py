"""Configuration management for Labelit."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os
import yaml


@dataclass
class Config:
    """Configuration for Labelit service."""

    monitored_folder: str
    aws_region: str
    bedrock_model_id: str
    log_level: str
    process_existing_on_startup: bool


class ConfigManager:
    """Manages loading, saving, and validating configuration."""

    DEFAULT_CONFIG_DIR = Path.home() / ".labelit"
    DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"

    @staticmethod
    def load_config(config_path: Optional[Path] = None) -> Config:
        """Load configuration from file or create default if missing."""
        if config_path is None:
            config_path = ConfigManager.DEFAULT_CONFIG_FILE

        if not config_path.exists():
            return ConfigManager.create_default_config(config_path)

        with open(config_path, "r") as f:
            data = yaml.safe_load(f)

        return Config(
            monitored_folder=os.path.expanduser(data.get("monitored_folder", "~/Pictures")),
            aws_region=data.get("aws_region", "us-east-1"),
            bedrock_model_id=data.get(
                "bedrock_model_id", "anthropic.claude-3-sonnet-20240229-v1:0"
            ),
            log_level=data.get("log_level", "INFO"),
            process_existing_on_startup=data.get("process_existing_on_startup", True),
        )

    @staticmethod
    def create_default_config(config_path: Optional[Path] = None) -> Config:
        """Create a default configuration file."""
        if config_path is None:
            config_path = ConfigManager.DEFAULT_CONFIG_FILE

        # Create config directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Determine default monitored folder based on OS
        if os.name == "nt":  # Windows
            default_folder = str(Path.home() / "Pictures")
        else:  # macOS and Linux
            default_folder = str(Path.home() / "Pictures")

        default_config = {
            "monitored_folder": default_folder,
            "aws_region": "us-east-1",
            "bedrock_model_id": "amazon.nova-lite-v1:0",
            "log_level": "INFO",
            "process_existing_on_startup": True,
        }

        with open(config_path, "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)

        return Config(
            monitored_folder=default_folder,
            aws_region="us-east-1",
            bedrock_model_id="amazon.nova-lite-v1:0",
            log_level="INFO",
            process_existing_on_startup=True,
        )

    @staticmethod
    def validate_config(config: Config) -> bool:
        """Validate configuration settings."""
        # Check if monitored folder exists
        if not Path(config.monitored_folder).exists():
            return False

        # Check if monitored folder is accessible
        if not os.access(config.monitored_folder, os.R_OK | os.W_OK):
            return False

        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config.log_level.upper() not in valid_log_levels:
            return False

        return True
