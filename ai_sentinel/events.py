"""
Event context and model definitions.

Defines the data structures used to represent security and evaluation events
captured by the SDK before transmission to the backend.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Any

from ai_sentinel.utils import generate_uuid, utc_now


@dataclass(frozen=True)
class EventContext:
    """Mutable-stage capture data flowing through the event pipeline.

    Attributes:
        prompt: Input prompt sent to the model or agent.
        response: Output returned by the model or agent.
        framework: Name of the AI framework or integration source.
        metadata: Arbitrary key-value context attached to the event.
        session_id: Identifier of the session that produced this event.
        trace_id: Distributed trace identifier for correlated observability.
        span_id: Span identifier within the active trace.
        event_id: Unique identifier for this event; assigned by processors.
        timestamp: UTC timestamp when the event was created; assigned by
            processors.
    """

    prompt: str
    response: str
    framework: str = "custom"
    metadata: dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    trace_id: str = ""
    span_id: str = ""
    event_id: str = ""
    timestamp: datetime | None = None

    def with_updates(self, **kwargs: Any) -> EventContext:
        """Return a copy of this context with the given fields replaced.

        Args:
            **kwargs: Field names and values to update.

        Returns:
            A new :class:`EventContext` instance with updated fields.
        """
        return replace(self, **kwargs)

    def to_event(self) -> Event:
        """Materialize a finalized :class:`Event` from this context.

        Returns:
            A fully populated :class:`Event` instance.

        Raises:
            ValueError: If required identifiers or timestamps are missing.
        """
        if not self.event_id:
            raise ValueError("event_id must be set before materializing an Event.")
        if self.timestamp is None:
            raise ValueError("timestamp must be set before materializing an Event.")

        return Event(
            event_id=self.event_id,
            session_id=self.session_id,
            trace_id=self.trace_id,
            span_id=self.span_id,
            timestamp=self.timestamp,
            framework=self.framework,
            prompt=self.prompt,
            response=self.response,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class Event:
    """Structured capture event for AI Sentinel.

    Attributes:
        event_id: Unique identifier for this event.
        session_id: Identifier of the session that produced this event.
        trace_id: Distributed trace identifier for correlated observability.
        span_id: Span identifier within the active trace.
        timestamp: UTC timestamp when the event was created.
        framework: Name of the AI framework or integration source.
        prompt: Input prompt sent to the model or agent.
        response: Output returned by the model or agent.
        metadata: Arbitrary key-value context attached to the event.
    """

    event_id: str
    session_id: str
    trace_id: str
    span_id: str
    timestamp: datetime
    framework: str
    prompt: str
    response: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the event to a dictionary suitable for transmission.

        Returns:
            Dictionary representation of this event.
        """
        return {
            "event_id": self.event_id,
            "session_id": self.session_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "timestamp": self.timestamp.isoformat(),
            "framework": self.framework,
            "prompt": self.prompt,
            "response": self.response,
            "metadata": self.metadata,
        }


def create_capture_event(
    session_id: str,
    trace_id: str,
    span_id: str,
    prompt: str,
    response: str,
    framework: str = "custom",
    metadata: dict[str, Any] | None = None,
) -> Event:
    """Build a capture event with generated identifiers and timestamps.

    Args:
        session_id: Active session identifier associated with the event.
        trace_id: Distributed trace identifier for the event.
        span_id: Span identifier within the active trace.
        prompt: Input prompt sent to the model or agent.
        response: Output returned by the model or agent.
        framework: Name of the AI framework or integration source.
        metadata: Optional additional context for the event.

    Returns:
        A fully populated :class:`Event` instance.
    """
    return Event(
        event_id=generate_uuid(),
        session_id=session_id,
        trace_id=trace_id,
        span_id=span_id,
        timestamp=utc_now(),
        framework=framework,
        prompt=prompt,
        response=response,
        metadata=dict(metadata or {}),
    )
