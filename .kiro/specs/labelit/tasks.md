# Implementation Plan

- [x] 1. Set up project structure and dependencies



  - Create Python package structure with proper modules
  - Set up pyproject.toml or setup.py with dependencies: watchdog, boto3, Pillow, PyYAML, hypothesis, pytest
  - Create basic directory structure: src/labelit/, tests/, config/
  - _Requirements: All_

- [x] 2. Implement configuration management


  - Create Config dataclass for configuration schema
  - Implement ConfigManager.load_config() to read from ~/.labelit/config.yaml
  - Implement ConfigManager.create_default_config() to generate default configuration
  - Implement ConfigManager.validate_config() to check paths and required fields
  - Support environment variable overrides for AWS credentials
  - _Requirements: 7.1, 7.2, 7.3_

- [ ]* 2.1 Write property test for configuration loading
  - **Property 20: Configuration loading**
  - **Validates: Requirements 7.1**

- [ ]* 2.2 Write property test for environment variable precedence
  - **Property 21: Environment variable precedence**
  - **Validates: Requirements 7.2**

- [ ]* 2.3 Write property test for default configuration creation
  - **Property 22: Default configuration creation**
  - **Validates: Requirements 7.3**

- [x] 3. Implement filename sanitization and generation


  - Create ImageAnalyzer class with sanitize_filename() method
  - Implement lowercase conversion logic
  - Implement space-to-hyphen replacement
  - Implement special character removal (keep only alphanumeric and hyphens)
  - Implement length limiting (max 50 characters)
  - Implement first phrase extraction for multi-sentence descriptions
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ]* 3.1 Write property test for filename length constraint
  - **Property 8: Filename length constraint**
  - **Validates: Requirements 3.1**

- [ ]* 3.2 Write property test for lowercase conversion
  - **Property 9: Lowercase conversion**
  - **Validates: Requirements 3.2**

- [ ]* 3.3 Write property test for space to hyphen conversion
  - **Property 10: Space to hyphen conversion**
  - **Validates: Requirements 3.3**

- [ ]* 3.4 Write property test for special character removal
  - **Property 11: Special character removal**
  - **Validates: Requirements 3.4**

- [ ]* 3.5 Write property test for first phrase extraction
  - **Property 12: First phrase extraction**
  - **Validates: Requirements 3.5**

- [x] 4. Implement file collision handling


  - Create FileRenamer class with collision detection
  - Implement check_collision() with OS-specific case sensitivity
  - Implement resolve_collision() to append numeric suffixes (-2, -3, etc.)
  - Handle edge cases (existing suffixes, multiple collisions)
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ]* 4.1 Write property test for collision suffix starting at 2
  - **Property 13: Collision suffix starts at 2**
  - **Validates: Requirements 4.1**

- [ ]* 4.2 Write property test for collision suffix increment
  - **Property 14: Collision suffix increment**
  - **Validates: Requirements 4.2**

- [ ]* 4.3 Write property test for OS-specific case sensitivity
  - **Property 15: OS-specific case sensitivity**
  - **Validates: Requirements 4.3, 4.4**

- [x] 5. Implement screenshot pattern matching


  - Create FileMonitor class with pattern matching logic
  - Implement OS detection (Windows, macOS, Linux)
  - Implement get_screenshot_patterns() for each OS
  - Implement is_screenshot() to match filenames against patterns
  - Support multiple patterns per OS
  - _Requirements: 1.2, 1.3, 1.4, 1.5, 6.4_

- [ ]* 5.1 Write property test for screenshot pattern recognition
  - **Property 2: Screenshot pattern recognition**
  - **Validates: Requirements 1.2, 1.3, 1.4, 1.5**

- [ ]* 5.2 Write property test for OS detection and pattern selection
  - **Property 19: OS detection and pattern selection**
  - **Validates: Requirements 6.4**

- [x] 6. Implement AWS Bedrock integration


  - Create ImageAnalyzer.analyze_image() method
  - Set up boto3 client for Bedrock Runtime
  - Implement image encoding (base64) for API requests
  - Create prompt template for filename generation
  - Implement response parsing to extract description
  - _Requirements: 2.1, 2.2_

- [ ]* 6.1 Write property test for AWS Bedrock invocation
  - **Property 3: AWS Bedrock invocation**
  - **Validates: Requirements 2.1**

- [ ]* 6.2 Write property test for description request format
  - **Property 4: Description request format**
  - **Validates: Requirements 2.2**

- [x] 7. Implement retry logic and fallback naming


  - Implement exponential backoff retry logic (3 attempts: 1s, 2s, 4s)
  - Add timeout handling (30 seconds per request)
  - Implement get_fallback_filename() with timestamp format
  - Handle all AWS error types (network, auth, rate limit, timeout)
  - _Requirements: 2.4, 2.5_

- [ ]* 7.1 Write property test for retry with exponential backoff
  - **Property 6: Retry with exponential backoff**
  - **Validates: Requirements 2.4**

- [ ]* 7.2 Write property test for fallback filename format
  - **Property 7: Fallback filename format**
  - **Validates: Requirements 2.5**

- [x] 8. Implement file system monitoring


  - Set up watchdog Observer and FileSystemEventHandler
  - Implement file creation event handling
  - Add debouncing logic (500ms delay after file creation)
  - Filter for image extensions (.png, .jpg, .jpeg)
  - Implement start() and stop() methods for monitoring
  - _Requirements: 1.1_

- [ ]* 8.1 Write property test for file detection timeliness
  - **Property 1: File detection timeliness**
  - **Validates: Requirements 1.1**

- [x] 9. Implement file renaming with logging


  - Create FileRenamer.rename_file() method
  - Implement atomic file rename operations
  - Add comprehensive logging for all operations
  - Log successful renames with old and new names
  - Log errors and continue processing
  - _Requirements: 5.3, 5.4_

- [ ]* 9.1 Write property test for operation logging completeness
  - **Property 17: Operation logging completeness**
  - **Validates: Requirements 5.3, 5.4**

- [x] 10. Implement startup file scanning


  - Create LabelitService.process_existing_files() method
  - Scan monitored folder for screenshot patterns
  - Process all matching files sequentially
  - Handle errors gracefully and continue processing
  - _Requirements: 5.1, 5.2_

- [ ]* 10.1 Write property test for startup scan completeness
  - **Property 16: Startup scan completeness**
  - **Validates: Requirements 5.1, 5.2**

- [x] 11. Implement main service orchestration


  - Create LabelitService class with start() and stop() methods
  - Implement startup sequence (load config, validate AWS, initialize components)
  - Implement file processing callback for monitor
  - Add signal handlers for graceful shutdown (SIGINT, SIGTERM)
  - Coordinate all components (monitor, analyzer, renamer)
  - _Requirements: All_

- [ ]* 11.1 Write property test for OS-specific path handling
  - **Property 18: OS-specific path handling**
  - **Validates: Requirements 6.1, 6.2, 6.3**

- [x] 12. Implement logging system


  - Set up Python logging with RotatingFileHandler
  - Configure log format, level, and rotation (10MB, 5 files)
  - Create log directory (~/.labelit/)
  - Implement structured logging for all operations
  - Ensure no sensitive data in logs
  - _Requirements: All_

- [x] 13. Implement error handling


  - Add try-catch blocks for all major operations
  - Implement graceful degradation for AWS failures
  - Add validation for configuration and credentials
  - Implement fail-fast for critical errors (missing config, invalid credentials)
  - Add helpful error messages with actionable guidance
  - _Requirements: 7.4, 7.5_

- [x] 14. Create CLI interface


  - Implement command-line argument parsing (argparse or click)
  - Add commands: start, stop, setup, version
  - Implement interactive setup wizard for first-run
  - Add --config flag for custom config path
  - Add --daemon flag for background execution
  - _Requirements: All_

- [x] 15. Add entry point and packaging


  - Create __main__.py for package execution
  - Set up entry points in pyproject.toml/setup.py
  - Configure PyInstaller spec for standalone executables
  - Test installation via pip
  - _Requirements: All_

- [x] 16. Checkpoint - Ensure all tests pass


  - Ensure all tests pass, ask the user if questions arise.

- [x] 17. Create documentation


  - Write README.md with installation and usage instructions
  - Document configuration options
  - Add AWS setup guide (credentials, Bedrock access)
  - Create troubleshooting guide
  - Add examples and screenshots
  - _Requirements: All_

- [x] 18. Final integration testing



  - Test end-to-end flow with real screenshots
  - Test with actual AWS Bedrock API
  - Test on multiple operating systems (Windows, macOS, Linux)
  - Test error scenarios (no internet, invalid credentials)
  - Test with various image formats and sizes
  - _Requirements: All_
