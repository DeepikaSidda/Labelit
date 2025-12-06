# Labelit 📸
<p align="center">
  <a href="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/kiro-2.jpg">
    <img src="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/kiro-2.jpg" width="650" />
  </a>
</p>


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

## 🎥 Watch the Video Demo

[![Watch the Demo on YouTube](https://img.youtube.com/vi/mec6PAQ0_Dg/maxresdefault.jpg)](https://youtu.be/mec6PAQ0_Dg)


## 📸 App Screenshots Gallery



| | |
|---|---|
| <a href="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/console-home-page-screens-hot-screenshot-of-a-labe-mh.png"><img src="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/console-home-page-screens-hot-screenshot-of-a-labe-mh.png" width="400"></a> | <a href="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/console-home-page-screenshot-with-various-colors.png"><img src="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/console-home-page-screenshot-with-various-colors.png" width="400"></a> |
| <a href="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/dragon-chinese-mythical-creature-illustration-art--mh.png"><img src="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/dragon-chinese-mythical-creature-illustration-art--mh.png" width="400"></a> | <a href="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/kiro-ghost-logo-logo-black-background-white-text.png"><img src="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/kiro-ghost-logo-logo-black-background-white-text.png" width="400"></a> |


<p align="center">
  <a href="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/screenshot-of-a-labelit-service-log-mh.png">
    <img src="https://raw.githubusercontent.com/DeepikaSidda/Labelit/main/Screenshots/screenshot-of-a-labelit-service-log-mh.png" width="650">
  </a>
  <br>
  <sub>🔹 Real-time Labelit service log showing screenshots automatically detected & renamed using AWS Bedrock.</sub><br>
  <sub>🔹 Labelit service log output – file rename events with AI-generated filenames.</sub>
</p>





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

```

## ⚡ Quick Start

```bash

# 1. Configure AWS
aws configure

# 2. Setup Labelit
labelit setup

# 3. Edit config file and change monitored_folder to YOUR screenshots folder
# Windows: notepad C:\Users\%USERNAME%\.labelit\config.yaml
# Mac/Linux: nano ~/.labelit/config.yaml

# 4. Start service
labelit start

# 5. Take a screenshot and watch it get renamed!
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
