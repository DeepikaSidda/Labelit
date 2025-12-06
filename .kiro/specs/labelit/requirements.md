# Requirements Document

## Introduction

Labelit is a lightweight Python background service that automatically renames screenshot files to descriptive names using AWS Bedrock's multimodal AI capabilities. The system runs as a simple daemon that monitors a designated folder for new screenshot files, analyzes the image content using AWS Bedrock, and automatically renames files with clean, descriptive names. No UI or database required - just a simple, automatic tool.

## Glossary

- **Labelit Service**: The background Python daemon that monitors folders and renames screenshots automatically
- **AWS Bedrock Service**: The Amazon Web Services multimodal AI service that analyzes images and generates descriptive text
- **Screenshot Pattern**: A filename pattern that identifies screenshot files from different operating systems
- **Monitored Folder**: The directory path configured for automatic file monitoring (typically user's Pictures or Screenshots folder)
- **Filename Collision**: A condition where a generated filename already exists in the target directory
- **Clean Filename Format**: A standardized format using lowercase letters, hyphens as separators, and excluding special characters
- **AWS Credentials**: The access key and secret key required to authenticate with AWS Bedrock Service, configured via environment variables or AWS CLI

## Requirements

### Requirement 1

**User Story:** As a user, I want the system to automatically detect new screenshot files in my monitored folder, so that I don't have to manually trigger the renaming process.

#### Acceptance Criteria

1. WHEN a new file with extension .png, .jpg, or .jpeg is created in the Monitored Folder, THE Labelit System SHALL detect the file within 2 seconds
2. WHEN a file matches the pattern "Screenshot*.png" on Windows, THE File Monitor SHALL identify it as a screenshot candidate
3. WHEN a file matches the pattern "Screen Shot*.png" on macOS, THE File Monitor SHALL identify it as a screenshot candidate
4. WHEN a file matches the pattern "Screenshot*.png" on Linux, THE File Monitor SHALL identify it as a screenshot candidate
5. WHEN a file matches the pattern "screenshot_*.png", THE File Monitor SHALL identify it as a screenshot candidate

### Requirement 2

**User Story:** As a user, I want the system to analyze images using AWS Bedrock's multimodal AI, so that descriptive filenames can be generated from both visual content and text.

#### Acceptance Criteria

1. WHEN an image file is detected, THE Image Analysis Engine SHALL send the image to AWS Bedrock Service for analysis
2. WHEN AWS Bedrock Service analyzes an image, THE Image Analysis Engine SHALL request a brief description of the image content suitable for a filename
3. WHEN AWS Bedrock Service returns a description, THE Labelit System SHALL generate a filename from the description within 10 seconds
4. WHEN the AWS Bedrock Service request fails, THE Labelit System SHALL retry the request up to 3 times with exponential backoff
5. WHEN all retry attempts fail, THE Labelit System SHALL generate a fallback filename using the pattern "image-YYYY-MM-DD-HHMMSS" where YYYY-MM-DD-HHMMSS represents the file creation timestamp

### Requirement 3

**User Story:** As a user, I want generated filenames to be clean and readable, so that my files are easy to identify and organize.

#### Acceptance Criteria

1. WHEN the Labelit System generates a filename from OCR text, THE Labelit System SHALL limit the filename to a maximum of 50 characters excluding the file extension
2. WHEN the Labelit System generates a filename, THE Labelit System SHALL convert all characters to lowercase
3. WHEN the Labelit System generates a filename, THE Labelit System SHALL replace spaces with hyphens
4. WHEN the Labelit System generates a filename, THE Labelit System SHALL remove all special characters except hyphens and alphanumeric characters
5. WHEN the OCR text contains multiple sentences, THE Labelit System SHALL use only the first meaningful phrase for the filename

### Requirement 4

**User Story:** As a user, I want the system to handle filename collisions automatically, so that existing files are not overwritten.

#### Acceptance Criteria

1. WHEN a generated filename already exists in the target directory, THE Labelit System SHALL append a numeric suffix starting with 2
2. WHEN a filename with a numeric suffix already exists, THE Labelit System SHALL increment the suffix until a unique filename is found
3. WHEN checking for filename collisions, THE Labelit System SHALL compare filenames in a case-insensitive manner on Windows and macOS
4. WHEN checking for filename collisions, THE Labelit System SHALL compare filenames in a case-sensitive manner on Linux

### Requirement 5

**User Story:** As a user, I want to process existing screenshot files when the service starts, so that I can rename screenshots that were created before the service was running.

#### Acceptance Criteria

1. WHEN the Labelit Service starts, THE Labelit Service SHALL scan the Monitored Folder for all files matching screenshot patterns
2. WHEN startup scanning is active, THE Labelit Service SHALL process all identified files sequentially
3. WHEN a file is successfully renamed, THE Labelit Service SHALL log the operation with original and new filenames
4. WHEN a file rename fails, THE Labelit Service SHALL log the error and continue processing remaining files

### Requirement 6

**User Story:** As a user, I want the tool to work consistently across Windows, macOS, and Linux, so that I can use it on any operating system.

#### Acceptance Criteria

1. WHEN the Labelit Service runs on Windows, THE Labelit Service SHALL use Windows-compatible path separators and file operations
2. WHEN the Labelit Service runs on macOS, THE Labelit Service SHALL use macOS-compatible path separators and file operations
3. WHEN the Labelit Service runs on Linux, THE Labelit Service SHALL use Linux-compatible path separators and file operations
4. WHEN the Labelit Service starts, THE Labelit Service SHALL detect the operating system and apply appropriate screenshot patterns

### Requirement 7

**User Story:** As a user, I want to configure the service using a simple configuration file or environment variables, so that I can set up the tool without complex installation.

#### Acceptance Criteria

1. WHEN the Labelit Service starts, THE Labelit Service SHALL read configuration from a config file in the user's home directory
2. WHERE AWS Credentials are configured via environment variables, THE Labelit Service SHALL use environment variables for AWS authentication
3. WHEN the configuration file is missing, THE Labelit Service SHALL create a default configuration file with the user's Pictures folder as the Monitored Folder
4. WHEN AWS Credentials are not found, THE Labelit Service SHALL log an error and exit with a helpful message
5. WHEN the Monitored Folder path in configuration does not exist, THE Labelit Service SHALL log an error and exit
