"""
Unit tests for event validators.
"""

from __future__ import annotations

import pytest

from ai_sentinel.events import EventContext
from ai_sentinel.exceptions import ValidationError
from ai_sentinel.validators.capture import CaptureInputValidator


class TestCaptureInputValidator:
    """Tests for capture input validation."""

    def test_validate_accepts_valid_context(self) -> None:
        validator = CaptureInputValidator()
        context = EventContext(
            prompt="Hello",
            response="Hi!",
            framework="custom",
            session_id="session-1",
            trace_id="trace-1",
            span_id="span-1",
        )

        validator.validate(context)

    def test_validate_rejects_empty_prompt(self) -> None:
        validator = CaptureInputValidator()
        context = EventContext(prompt="  ", response="Hi!", framework="custom")

        with pytest.raises(ValidationError, match="prompt is required"):
            validator.validate(context)

    def test_validate_rejects_empty_response(self) -> None:
        validator = CaptureInputValidator()
        context = EventContext(prompt="Hello", response="", framework="custom")

        with pytest.raises(ValidationError, match="response is required"):
            validator.validate(context)

    def test_validate_rejects_empty_framework(self) -> None:
        validator = CaptureInputValidator()
        context = EventContext(prompt="Hello", response="Hi!", framework="  ")

        with pytest.raises(ValidationError, match="framework is required"):
            validator.validate(context)
