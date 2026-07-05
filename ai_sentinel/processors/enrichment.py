"""
Event enrichment processor for the AI Sentinel event pipeline.

Assigns event identifiers and timestamps to contexts that already carry session,
trace, and span identifiers from the instrumentation layer.
"""

from __future__ import annotations

from ai_sentinel.events import EventContext
from ai_sentinel.logging_config import get_logger
from ai_sentinel.utils import generate_uuid, utc_now

logger = get_logger("processors.enrichment")


class EventEnrichmentProcessor:
    """Enriches event contexts with generated event identifiers and timestamps."""

    def process(self, context: EventContext) -> EventContext:
        """Assign ``event_id`` and ``timestamp`` when not already present.

        Args:
            context: Capture data to enrich.

        Returns:
            An updated :class:`EventContext` with identity fields populated.
        """
        event_id = context.event_id or generate_uuid()
        timestamp = context.timestamp or utc_now()

        logger.debug(
            "Event enriched event_id=%s trace_id=%s span_id=%s session_id=%s",
            event_id,
            context.trace_id,
            context.span_id,
            context.session_id,
        )

        return context.with_updates(event_id=event_id, timestamp=timestamp)
