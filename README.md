# Labelit 📸

Labelit is a lightweight Python background service that automatically renames screenshot files to descriptive names using AWS Bedrock's multimodal AI capabilities.

**Example:** `Screenshot 2024-12-05.png` → `google-homepage-with-custom-shortcuts.png`

## ✨ Features

- 🤖 **AI-Powered Renaming**: Uses AWS Bedrock (Amazon Nova Lite - FREE!) to analyze images and generate descriptive filenames
- 📁 **Automatic Monitoring**: Watches your screenshots folder and processes new files automatically
- 🔄 **Cross-Platform**: Works on Windows, macOS, and Linux
- 🎯 **Smart Collision Handling**: Automatically handles filename conflicts
- 📝 **Clean Filenames**: Generates lowercase, hyphenated filenames without special characters
- ⚡ **Lightweight**: No database, no UI - just a simple background service
- 💰 **Completely FREE**: Uses Amazon Nova Lite - no cost per screenshot!


## 📋 Requirements

- Python 3.9 or higher
- AWS account with Bedrock access enabled
- Internet connection for AWS Bedrock API

## 🔧 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/labelit.git
cd labelit

# Install dependencies
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## ⚡ Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure AWS
aws configure

# 3. Setup Labelit
labelit setup

# 4. Edit config file and change monitored_folder to YOUR screenshots folder
# Windows: notepad C:\Users\%USERNAME%\.labelit\config.yaml
# Mac/Linux: nano ~/.labelit/config.yaml

# 5. Start service
labelit start

# 6. Take a screenshot and watch it get renamed!
```


## Configuration

### 1. Set up AWS Credentials

Configure your AWS credentials using one of these methods:

```bash
aws configure
```

### 2. Initialize Labelit

```bash
labelit setup
```

This creates a configuration file at `~/.labelit/config.yaml` with default settings:

```yaml
monitored_folder: ~/Pictures
aws_region: us-east-1
bedrock_model_id: amazon.nova-lite-v1:0
log_level: INFO
process_existing_on_startup: true
```

You can edit this file to customize the settings.

## Usage

### Start the Service

```bash
labelit start
```

The service will:
1. Process any existing screenshots in the monitored folder (if configured)
2. Start monitoring for new screenshot files
3. Automatically rename new screenshots as they appear

### Stop the Service

Press `Ctrl+C` to stop the service gracefully.

## How It Works

1. **Detection**: Labelit monitors your configured folder for new files matching screenshot patterns:
   - Windows: `Screenshot*.png`, `screenshot_*.png`
   - macOS: `Screen Shot*.png`
   - Linux: `Screenshot*.png`

2. **Analysis**: When a screenshot is detected, it's sent to AWS Bedrock for analysis

3. **Renaming**: The AI generates a description, which is converted to a clean filename:
   - Lowercase letters only
   - Spaces replaced with hyphens
   - Special characters removed
   - Maximum 50 characters
   - Example: `Screenshot 2024-12-05.png` → `login-screen-with-username-field.png`

4. **Collision Handling**: If a filename already exists, a numeric suffix is added:
   - `login-screen.png` → `login-screen-2.png` → `login-screen-3.png`


## Logs

Logs are stored at `~/.labelit/labelit.log` with automatic rotation (10MB max, 5 backup files).

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/labelit --cov-report=html

# Run property-based tests
pytest tests/ -k property
```

### Code Formatting

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```
