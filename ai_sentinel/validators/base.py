"""
Validator protocol for the AI Sentinel event pipeline.

Defines the contract that all validators must implement so the pipeline can
accept custom validation strategies without modification.
"""

from __future__ import annotations

from typing import Protocol

from ai_sentinel.events import EventContext


class Validator(Protocol):
    """Contract for event context validation steps."""

    def validate(self, context: EventContext) -> None:
        """Validate an event context before processing.

        Args:
            context: Capture data to validate.

        Raises:
            ValidationError: If the context fails validation rules.
        """
        ...
