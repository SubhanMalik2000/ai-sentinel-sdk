"""
Processor contracts and exports for the AI Sentinel event pipeline.

Processors transform :class:`~ai_sentinel.events.EventContext` instances as
they move toward materialization and delivery.
"""

from ai_sentinel.processors.base import Processor
from ai_sentinel.processors.enrichment import EventEnrichmentProcessor

__all__ = [
    "EventEnrichmentProcessor",
    "Processor",
]
