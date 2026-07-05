"""
Unit tests for instrumentation components.
"""

from __future__ import annotations

from uuid import UUID

from ai_sentinel.instrumentation.decorators import observe, trace
from ai_sentinel.instrumentation.session import SessionManager
from ai_sentinel.instrumentation.trace import TraceManager


class TestTraceManager:
    """Tests for trace and span identifier management."""

    def test_start_span_creates_trace_and_span_ids(self) -> None:
        manager = TraceManager()
        context = manager.start_span()

        UUID(context.trace_id)
        UUID(context.span_id)
        assert manager.trace_id == context.trace_id

    def test_start_span_reuses_trace_id(self) -> None:
        manager = TraceManager()
        first = manager.start_span()
        second = manager.start_span()

        assert first.trace_id == second.trace_id
        assert first.span_id != second.span_id

    def test_reset_trace_starts_new_trace(self) -> None:
        manager = TraceManager()
        first = manager.start_span()
        manager.reset_trace()
        second = manager.start_span()

        assert first.trace_id != second.trace_id


class TestSessionManager:
    """Tests for session identifier management."""

    def test_create_session_generates_session_id(self) -> None:
        manager = SessionManager()
        session = manager.create_session()

        UUID(session.session_id)
        assert session.created_at.tzinfo is not None
        assert manager.current == session

    def test_get_or_create_session_reuses_active_session(self) -> None:
        manager = SessionManager()
        first = manager.get_or_create_session()
        second = manager.get_or_create_session()

        assert first.session_id == second.session_id


class TestDecorators:
    """Tests for instrumentation decorator placeholders."""

    def test_trace_decorator_preserves_behavior(self) -> None:
        @trace("sample")
        def add(a: int, b: int) -> int:
            return a + b

        assert add(2, 3) == 5

    def test_observe_decorator_preserves_behavior(self) -> None:
        @observe("sample")
        def multiply(a: int, b: int) -> int:
            return a * b

        assert multiply(2, 3) == 6
