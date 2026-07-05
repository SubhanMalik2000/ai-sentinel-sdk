"""
Unit tests for the event pipeline.

Validates the validator-processor-sender orchestration and default factory.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from ai_sentinel.config import Config
from ai_sentinel.events import EventContext
from ai_sentinel.exceptions import ValidationError
from ai_sentinel.pipeline import EventPipeline, create_default_pipeline
from ai_sentinel.processors.enrichment import EventEnrichmentProcessor
from ai_sentinel.sender import EventSender
from ai_sentinel.validators.capture import CaptureInputValidator


class RecordingSender(EventSender):
    """Test double that records events without printing them."""

    def __init__(self) -> None:
        super().__init__(Config(api_key="sk_test", verbose=False))
        self.sent_events: list = []

    def send(self, event) -> None:
        self.sent_events.append(event)


class TestEventPipeline:
    """Tests for pipeline orchestration."""

    def test_execute_runs_validator_processor_sender(self) -> None:
        sender = RecordingSender()
        pipeline = EventPipeline(
            validators=[CaptureInputValidator()],
            processors=[EventEnrichmentProcessor()],
            sender=sender,
        )
        context = EventContext(
            prompt="Hello",
            response="Hi!",
            session_id="session-1",
            trace_id="trace-1",
            span_id="span-1",
        )

        event = pipeline.execute(context)

        assert len(sender.sent_events) == 1
        assert sender.sent_events[0] == event
        UUID(event.event_id)
        assert event.trace_id == "trace-1"
        assert event.span_id == "span-1"

    def test_execute_raises_when_validation_fails(self) -> None:
        sender = RecordingSender()
        pipeline = EventPipeline(
            validators=[CaptureInputValidator()],
            processors=[EventEnrichmentProcessor()],
            sender=sender,
        )
        context = EventContext(
            prompt="",
            response="Hi!",
            session_id="session-1",
            trace_id="trace-1",
            span_id="span-1",
        )

        with pytest.raises(ValidationError, match="prompt is required"):
            pipeline.execute(context)

        assert sender.sent_events == []

    def test_create_default_pipeline_builds_standard_chain(self) -> None:
        config = Config(api_key="sk_test", verbose=False)
        pipeline = create_default_pipeline(config)

        assert len(pipeline.validators) == 1
        assert isinstance(pipeline.validators[0], CaptureInputValidator)
        assert len(pipeline.processors) == 1
        assert isinstance(pipeline.processors[0], EventEnrichmentProcessor)
