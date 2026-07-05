"""
Event transmission module.

Responsible for delivering events from the SDK to the AI Sentinel backend.
Sprint 3 uses local pretty-printing only; HTTP transport arrives in a
future sprint.
"""

from __future__ import annotations

import json
from typing import Protocol

from ai_sentinel.config import Config
from ai_sentinel.events import Event
from ai_sentinel.logging_config import get_logger

logger = get_logger("sender")


class EventTransport(Protocol):
    """Protocol for event delivery implementations."""

    def send(self, event: Event) -> None:
        """Deliver a structured event.

        Args:
            event: Event instance to deliver.
        """
        ...


class EventSender:
    """Responsible for sending events to a transport backend."""

    def __init__(self, config: Config) -> None:
        """Initialize the event sender.

        Args:
            config: SDK configuration used for endpoint and transport settings.
        """
        self._config = config

    def send(self, event: Event) -> None:
        """Pretty-print a structured event to stdout.

        Args:
            event: Event instance to display.

        Note:
            Sprint 3 does not perform HTTP requests. Future sprints will extend
            this class or swap in an HTTP-backed transport implementation.
        """
        logger.info(
            "Event sent event_id=%s session_id=%s trace_id=%s span_id=%s",
            event.event_id,
            event.session_id,
            event.trace_id,
            event.span_id,
        )
        print(self.format_event(event))

    def format_event(self, event: Event) -> str:
        """Format an event as indented JSON.

        Args:
            event: Event instance to serialize.

        Returns:
            Pretty-printed JSON string for the event payload.
        """
        return json.dumps(event.to_dict(), indent=2, sort_keys=True)
