"""Main entry point for Labelit."""

import argparse
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .config import Config, ConfigManager
from .service import LabelitService


def setup_logging(config: Config) -> None:
    """
    Set up logging configuration.

    Args:
        config: Configuration object
    """
    # Create log directory
    log_dir = Path.home() / ".labelit"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "labelit.log"

    # Configure logging
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def validate_aws_credentials() -> bool:
    """
    Validate that AWS credentials are available.

    Returns:
        True if credentials are found
    """
    import os
    import boto3

    # Check environment variables
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        return True

    # Check AWS credentials file
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            return True
    except Exception:
        pass

    return False


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Labelit - Automatic screenshot renaming using AWS Bedrock AI"
    )
    parser.add_argument(
        "command",
        choices=["start", "setup", "version"],
        help="Command to execute",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to configuration file (default: ~/.labelit/config.yaml)",
    )

    args = parser.parse_args()

    if args.command == "version":
        from . import __version__

        print(f"Labelit version {__version__}")
        return

    if args.command == "setup":
        print("Setting up Labelit...")
        config = ConfigManager.create_default_config(args.config)
        print(f"Configuration created at: {ConfigManager.DEFAULT_CONFIG_FILE}")
        print(f"Monitored folder: {config.monitored_folder}")
        print("\nPlease configure your AWS credentials:")
        print("  - Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        print("  - Or configure ~/.aws/credentials file")
        print("\nThen run: labelit start")
        return

    # Load configuration
    try:
        config = ConfigManager.load_config(args.config)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        print("Run 'labelit setup' to create a default configuration", file=sys.stderr)
        sys.exit(1)

    # Set up logging
    setup_logging(config)
    logger = logging.getLogger(__name__)

    # Validate configuration
    if not ConfigManager.validate_config(config):
        logger.error(f"Invalid configuration: Monitored folder does not exist or is not accessible")
        logger.error(f"Monitored folder: {config.monitored_folder}")
        sys.exit(1)

    # Validate AWS credentials
    if not validate_aws_credentials():
        logger.error("AWS credentials not found!")
        logger.error("Please configure your AWS credentials:")
        logger.error("  - Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        logger.error("  - Or configure ~/.aws/credentials file")
        sys.exit(1)

    # Start service
    if args.command == "start":
        logger.info("Starting Labelit service...")
        service = LabelitService(config)
        try:
            service.start()
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            service.stop()
        except Exception as e:
            logger.error(f"Service error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == "__main__":
    main()
