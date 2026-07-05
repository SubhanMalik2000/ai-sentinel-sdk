"""
Unit tests for the Sentinel client.

Validates client initialization, session creation, event capture, and pipeline
integration without HTTP transport.
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID

import pytest

from ai_sentinel import Sentinel
from ai_sentinel.config import Config
from ai_sentinel.events import Event, EventContext, create_capture_event
from ai_sentinel.exceptions import ConfigurationError, ValidationError
from ai_sentinel.pipeline import EventPipeline, create_default_pipeline
from ai_sentinel.processors.enrichment import EventEnrichmentProcessor
from ai_sentinel.sender import EventSender
from ai_sentinel.session import SessionManager
from ai_sentinel.validators.capture import CaptureInputValidator


class CapturingSender(EventSender):
    """Test double that records events instead of printing them."""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.sent_events: list[Event] = []

    def send(self, event: Event) -> None:
        self.sent_events.append(event)


class TestConfig:
    """Tests for SDK configuration."""

    def test_validate_requires_api_key(self) -> None:
        config = Config(api_key=None)
        with pytest.raises(ConfigurationError, match="api_key is required"):
            config.validate()

    def test_validate_rejects_empty_api_key(self) -> None:
        config = Config(api_key="   ")
        with pytest.raises(ConfigurationError, match="api_key is required"):
            config.validate()


class TestEvent:
    """Tests for event models and factories."""

    def test_create_capture_event_generates_ids_and_timestamp(self) -> None:
        event = create_capture_event(
            session_id="session-123",
            trace_id="550e8400-e29b-41d4-a716-446655440000",
            span_id="6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            prompt="Hello",
            response="Hi!",
        )

        UUID(event.event_id)
        assert event.trace_id == "550e8400-e29b-41d4-a716-446655440000"
        assert event.span_id == "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
        assert event.session_id == "session-123"
        assert event.timestamp.tzinfo is not None
        assert event.framework == "custom"
        assert event.prompt == "Hello"
        assert event.response == "Hi!"
        assert event.metadata == {}

    def test_to_dict_contains_required_fields(self) -> None:
        event = create_capture_event(
            session_id="session-123",
            trace_id="trace-123",
            span_id="span-123",
            prompt="Hello",
            response="Hi!",
            framework="custom",
            metadata={"source": "test"},
        )
        payload = event.to_dict()

        assert set(payload) == {
            "event_id",
            "session_id",
            "trace_id",
            "span_id",
            "timestamp",
            "framework",
            "prompt",
            "response",
            "metadata",
        }
        assert payload["metadata"] == {"source": "test"}


class TestEventSender:
    """Tests for local event delivery."""

    def test_format_event_returns_pretty_json(self) -> None:
        event = create_capture_event(
            session_id="session-123",
            trace_id="trace-123",
            span_id="span-123",
            prompt="Hello",
            response="Hi!",
        )
        sender = EventSender(Config(api_key="sk_test", verbose=False))
        formatted = sender.format_event(event)

        parsed: dict[str, Any] = json.loads(formatted)
        assert parsed["prompt"] == "Hello"
        assert parsed["response"] == "Hi!"
        assert parsed["trace_id"] == "trace-123"
        assert parsed["span_id"] == "span-123"


class TestSentinel:
    """Tests for the Sentinel client class."""

    def test_initialization_prints_lifecycle_messages(self, capsys: pytest.CaptureFixture[str]) -> None:
        Sentinel(api_key="sk_test")

        captured = capsys.readouterr().out
        assert "SDK initialized." in captured
        assert "Session created." in captured

    def test_custom_config_initialization(self) -> None:
        config = Config(api_key="test-key", endpoint_url="https://example.com/v1", verbose=False)
        client = Sentinel(config=config)

        assert client.config.api_key == "test-key"
        assert client.session.session_id

    def test_capture_sends_structured_event(self) -> None:
        config = Config(api_key="sk_test", verbose=False)
        sender = CapturingSender(config)
        client = Sentinel(config=config, sender=sender)

        event = client.capture(prompt="Hello", response="Hi!")

        assert len(sender.sent_events) == 1
        assert sender.sent_events[0] == event
        assert event.prompt == "Hello"
        assert event.response == "Hi!"
        assert event.session_id == client.session.session_id
        UUID(event.trace_id)
        UUID(event.span_id)
        UUID(event.event_id)

    def test_capture_prints_structured_event(self, capsys: pytest.CaptureFixture[str]) -> None:
        client = Sentinel(config=Config(api_key="sk_test", verbose=False))

        client.capture(prompt="Hello", response="Hi!")

        captured = capsys.readouterr().out
        payload = json.loads(captured)
        assert payload["prompt"] == "Hello"
        assert payload["response"] == "Hi!"
        assert "trace_id" in payload
        assert "span_id" in payload

    def test_capture_rejects_empty_prompt(self) -> None:
        client = Sentinel(config=Config(api_key="sk_test", verbose=False))

        with pytest.raises(ValidationError, match="prompt is required"):
            client.capture(prompt="  ", response="Hi!")

    def test_capture_rejects_empty_response(self) -> None:
        client = Sentinel(config=Config(api_key="sk_test", verbose=False))

        with pytest.raises(ValidationError, match="response is required"):
            client.capture(prompt="Hello", response="")

    def test_conflicting_api_key_and_config_raise(self) -> None:
        with pytest.raises(ConfigurationError, match="Pass either api_key or config"):
            Sentinel(api_key="sk_test", config=Config(api_key="other"))

    def test_repr_contains_session_and_endpoint(self) -> None:
        client = Sentinel(config=Config(api_key="sk_test", verbose=False))

        representation = repr(client)
        assert "Sentinel(" in representation
        assert client.session.session_id in representation

    def test_custom_session_manager_is_used(self) -> None:
        manager = SessionManager()
        client = Sentinel(config=Config(api_key="sk_test", verbose=False), session_manager=manager)

        assert client.session.session_id
        assert manager.current == client.session

    def test_capture_uses_pipeline_not_sender_directly(self) -> None:
        config = Config(api_key="sk_test", verbose=False)
        sender = CapturingSender(config)
        pipeline = create_default_pipeline(config, sender)
        client = Sentinel(config=config, pipeline=pipeline)

        event = client.capture(prompt="Hello", response="Hi!")

        assert event.event_id
        assert len(sender.sent_events) == 1

    def test_custom_pipeline_is_used(self) -> None:
        config = Config(api_key="sk_test", verbose=False)
        sender = CapturingSender(config)
        pipeline = EventPipeline(
            validators=[CaptureInputValidator()],
            processors=[EventEnrichmentProcessor()],
            sender=sender,
        )
        client = Sentinel(config=config, pipeline=pipeline)

        client.capture(prompt="Hello", response="Hi!")
        assert len(sender.sent_events) == 1
