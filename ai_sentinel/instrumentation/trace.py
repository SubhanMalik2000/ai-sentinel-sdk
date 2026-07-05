"""
Distributed trace management for the AI Sentinel SDK.

Generates and tracks trace and span identifiers that propagate through the
event pipeline for correlated observability.
"""

from __future__ import annotations

from dataclasses import dataclass

from ai_sentinel.logging_config import get_logger
from ai_sentinel.utils import generate_uuid

logger = get_logger("instrumentation.trace")


@dataclass(frozen=True)
class TraceContext:
    """Immutable trace identifiers for a single pipeline execution.

    Attributes:
        trace_id: Identifier for the distributed trace.
        span_id: Identifier for the current span within the trace.
    """

    trace_id: str
    span_id: str


class TraceManager:
    """Creates and manages trace and span identifiers.

    Each :class:`TraceManager` instance owns one active trace. Calling
    :meth:`start_span` creates a new span while reusing the trace identifier
    until :meth:`reset_trace` is invoked.
    """

    def __init__(self) -> None:
        """Initialize an empty trace manager without an active trace."""
        self._trace_id: str | None = None

    @property
    def trace_id(self) -> str | None:
        """Return the active trace identifier, if any."""
        return self._trace_id

    def ensure_trace(self) -> str:
        """Return the active trace identifier, creating one when absent.

        Returns:
            The current trace identifier.
        """
        if self._trace_id is None:
            self._trace_id = generate_uuid()
            logger.debug("Trace started trace_id=%s", self._trace_id)
        return self._trace_id

    def start_span(self) -> TraceContext:
        """Start a new span within the active trace.

        Returns:
            A :class:`TraceContext` containing trace and span identifiers.
        """
        trace_id = self.ensure_trace()
        span_id = generate_uuid()
        logger.debug(
            "Span started trace_id=%s span_id=%s",
            trace_id,
            span_id,
        )
        return TraceContext(trace_id=trace_id, span_id=span_id)

    def reset_trace(self) -> None:
        """Clear the active trace so the next span starts a new trace."""
        if self._trace_id is not None:
            logger.debug("Trace reset trace_id=%s", self._trace_id)
        self._trace_id = None
