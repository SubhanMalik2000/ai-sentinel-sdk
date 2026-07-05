"""
SDK configuration module.

Centralizes all tunable settings for the AI Sentinel client, including
endpoint URLs, authentication credentials, and transport behavior.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from ai_sentinel.exceptions import ConfigurationError


@dataclass
class Config:
    """SDK configuration.

    Attributes:
        api_key: API key used to authenticate requests to the backend.
        endpoint_url: Base URL for the AI Sentinel API.
        timeout_seconds: HTTP request timeout in seconds.
        max_retries: Maximum number of retry attempts for failed requests.
        verbose: Whether the SDK prints lifecycle messages to stdout.
        log_level: Logging level for structured SDK log output.
        extra: Additional provider-specific or experimental settings.
    """

    api_key: str | None = None
    endpoint_url: str = "https://api.aisentinel.dev/v1"
    timeout_seconds: float = 30.0
    max_retries: int = 3
    verbose: bool = True
    log_level: int = logging.INFO
    extra: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration values.

        Raises:
            ConfigurationError: If required or malformed settings are detected.
        """
        if not self.api_key or not self.api_key.strip():
            raise ConfigurationError("api_key is required and cannot be empty.")

        if self.timeout_seconds <= 0:
            raise ConfigurationError("timeout_seconds must be greater than zero.")

        if self.max_retries < 0:
            raise ConfigurationError("max_retries cannot be negative.")

        if not self.endpoint_url.strip():
            raise ConfigurationError("endpoint_url cannot be empty.")
