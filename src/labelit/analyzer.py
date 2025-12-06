"""Image analysis and filename generation using AWS Bedrock."""

import base64
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
import boto3
from botocore.exceptions import ClientError


class ImageAnalyzer:
    """Analyzes images with AWS Bedrock and generates clean filenames."""

    def __init__(self, aws_region: str, model_id: str):
        """
        Initialize the image analyzer.

        Args:
            aws_region: AWS region for Bedrock service
            model_id: Bedrock model ID to use
        """
        self.aws_region = aws_region
        self.model_id = model_id
        self.client = None

    def _get_client(self):
        """Get or create boto3 Bedrock Runtime client."""
        if self.client is None:
            self.client = boto3.client("bedrock-runtime", region_name=self.aws_region)
        return self.client

    def analyze_image(self, image_path: str) -> str:
        """
        Analyze an image and get a description from AWS Bedrock.

        Args:
            image_path: Path to the image file

        Returns:
            Description text from Bedrock, or fallback filename on failure
        """
        # Try up to 3 times with exponential backoff
        delays = [1, 2, 4]

        for attempt, delay in enumerate(delays):
            try:
                # Read and encode image
                with open(image_path, "rb") as f:
                    image_data = f.read()

                image_base64 = base64.b64encode(image_data).decode("utf-8")

                # Determine request format based on model
                if "nova" in self.model_id.lower():
                    # Amazon Nova format - use converse API
                    client = self._get_client()
                    response = client.converse(
                        modelId=self.model_id,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "image": {
                                            "format": "png",
                                            "source": {"bytes": image_data}
                                        }
                                    },
                                    {
                                        "text": "Describe this image in 5-7 words suitable for a filename. Focus on the main content or purpose. Only provide the description, nothing else."
                                    }
                                ]
                            }
                        ],
                        inferenceConfig={
                            "maxTokens": 100,
                            "temperature": 0.5,
                            "topP": 0.9
                        }
                    )
                    
                    # Parse Nova response
                    description = response["output"]["message"]["content"][0]["text"]
                    return description
                elif "llama" in self.model_id.lower():
                    # Llama 3.2 Vision format
                    request_body = {
                        "prompt": f"<|image|>Describe this image in 5-7 words suitable for a filename. Focus on the main content or purpose.",
                        "max_gen_len": 100,
                        "temperature": 0.5,
                        "top_p": 0.9,
                    }
                else:
                    # Claude/Anthropic format
                    request_body = {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 100,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/png",
                                            "data": image_base64,
                                        },
                                    },
                                    {
                                        "type": "text",
                                        "text": "Describe this image in 5-7 words suitable for a filename. Focus on the main content or purpose.",
                                    },
                                ],
                            }
                        ],
                    }

                # Call Bedrock (for non-Nova models)
                if "nova" not in self.model_id.lower():
                    client = self._get_client()
                    response = client.invoke_model(
                        modelId=self.model_id,
                        body=json.dumps(request_body),
                        contentType="application/json",
                        accept="application/json",
                    )

                    # Parse response based on model
                    response_body = json.loads(response["body"].read())
                    
                    if "llama" in self.model_id.lower():
                        # Llama response format
                        description = response_body.get("generation", "")
                    else:
                        # Claude response format
                        description = response_body["content"][0]["text"]

                    return description

            except (ClientError, Exception) as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"AWS Bedrock request failed (attempt {attempt + 1}/3): {str(e)}")
                
                if attempt < len(delays) - 1:
                    # Wait before retry
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    # All retries failed, use fallback
                    logger.warning(f"All AWS Bedrock retries failed. Using fallback naming for {image_path}")
                    return self.get_fallback_filename(image_path)

        return self.get_fallback_filename(image_path)

    def generate_filename(self, description: str, original_ext: str) -> str:
        """
        Generate a clean filename from a description.

        Args:
            description: Text description from Bedrock
            original_ext: Original file extension (e.g., '.png')

        Returns:
            Clean filename with extension
        """
        clean_name = self.sanitize_filename(description)
        return f"{clean_name}{original_ext}"

    def sanitize_filename(self, text: str, max_length: int = 50) -> str:
        """
        Sanitize text to create a clean filename.

        Args:
            text: Input text to sanitize
            max_length: Maximum length for the filename (default 50)

        Returns:
            Sanitized filename string
        """
        # Take first sentence/phrase
        if "." in text:
            text = text.split(".")[0]

        # Convert to lowercase
        text = text.lower()

        # Replace spaces with hyphens
        text = text.replace(" ", "-")

        # Remove special characters (keep only alphanumeric and hyphens)
        clean_chars = []
        for char in text:
            if char.isalnum() or char == "-":
                clean_chars.append(char)

        text = "".join(clean_chars)

        # Collapse multiple hyphens into single hyphen
        while "--" in text:
            text = text.replace("--", "-")

        # Remove leading/trailing hyphens
        text = text.strip("-")

        # Limit length
        if len(text) > max_length:
            text = text[:max_length].rstrip("-")

        return text

    def get_fallback_filename(self, file_path: str) -> str:
        """
        Generate a fallback filename based on timestamp.

        Args:
            file_path: Path to the file

        Returns:
            Fallback filename in format 'image-YYYYMMDD-HHMMSS'
        """
        # Get file creation time
        path = Path(file_path)
        timestamp = datetime.fromtimestamp(path.stat().st_ctime)
        return timestamp.strftime("image-%Y%m%d-%H%M%S")
