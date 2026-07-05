"""
Capture input validator for the AI Sentinel event pipeline.

Validates required prompt, response, and framework fields on event contexts
before they enter the processor chain.
"""

from __future__ import annotations

from ai_sentinel.events import EventContext
from ai_sentinel.exceptions import ValidationError
from ai_sentinel.logging_config import get_logger

logger = get_logger("validators.capture")


class CaptureInputValidator:
    """Validates required capture fields on an :class:`EventContext`."""

    def validate(self, context: EventContext) -> None:
        """Validate capture inputs before event processing.

        Args:
            context: Capture data to validate.

        Raises:
            ValidationError: If any required field is empty.
        """
        if not context.prompt or not context.prompt.strip():
            logger.warning("Validation failed field=prompt reason=empty")
            raise ValidationError("prompt is required and cannot be empty.")

        if not context.response or not context.response.strip():
            logger.warning("Validation failed field=response reason=empty")
            raise ValidationError("response is required and cannot be empty.")

        if not context.framework or not context.framework.strip():
            logger.warning("Validation failed field=framework reason=empty")
            raise ValidationError("framework is required and cannot be empty.")

        logger.debug(
            "Capture input validated framework=%s session_id=%s",
            context.framework,
            context.session_id,
        )
