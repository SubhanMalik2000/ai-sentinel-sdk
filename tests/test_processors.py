"""
Unit tests for event processors.
"""

from __future__ import annotations

from uuid import UUID

from ai_sentinel.events import EventContext
from ai_sentinel.processors.enrichment import EventEnrichmentProcessor


class TestEventEnrichmentProcessor:
    """Tests for event identity enrichment."""

    def test_process_assigns_event_id_and_timestamp(self) -> None:
        processor = EventEnrichmentProcessor()
        context = EventContext(
            prompt="Hello",
            response="Hi!",
            session_id="session-1",
            trace_id="trace-1",
            span_id="span-1",
        )

        enriched = processor.process(context)

        UUID(enriched.event_id)
        assert enriched.timestamp is not None
        assert enriched.timestamp.tzinfo is not None

    def test_process_preserves_existing_event_id(self) -> None:
        processor = EventEnrichmentProcessor()
        context = EventContext(
            prompt="Hello",
            response="Hi!",
            event_id="fixed-event-id",
            session_id="session-1",
            trace_id="trace-1",
            span_id="span-1",
        )

        enriched = processor.process(context)

        assert enriched.event_id == "fixed-event-id"

    def test_process_materializes_event(self) -> None:
        processor = EventEnrichmentProcessor()
        context = EventContext(
            prompt="Hello",
            response="Hi!",
            session_id="session-1",
            trace_id="trace-1",
            span_id="span-1",
        )

        event = processor.process(context).to_event()

        assert event.prompt == "Hello"
        assert event.response == "Hi!"
        assert event.trace_id == "trace-1"
        assert event.span_id == "span-1"
