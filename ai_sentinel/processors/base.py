"""
Processor protocol for the AI Sentinel event pipeline.

Defines the contract that all processors must implement so the pipeline can
accept custom enrichment or transformation steps without modification.
"""

from __future__ import annotations

from typing import Protocol

from ai_sentinel.events import EventContext


class Processor(Protocol):
    """Contract for event context transformation steps."""

    def process(self, context: EventContext) -> EventContext:
        """Transform an event context and return the updated context.

        Args:
            context: Capture data to transform.

        Returns:
            The updated :class:`EventContext`, typically a new immutable copy.
        """
        ...
