"""
Main SDK client module.

Defines the primary ``Sentinel`` class that orchestrates configuration,
instrumentation, and the event pipeline for capture operations.
"""

from __future__ import annotations

from typing import Any

from ai_sentinel.config import Config
from ai_sentinel.events import Event, EventContext
from ai_sentinel.exceptions import ConfigurationError
from ai_sentinel.instrumentation.session import Session, SessionManager
from ai_sentinel.instrumentation.trace import TraceManager
from ai_sentinel.logging_config import configure_logging, get_logger
from ai_sentinel.pipeline import EventPipeline, create_default_pipeline
from ai_sentinel.sender import EventTransport

logger = get_logger("client")


class Sentinel:
    """Main SDK client for AI Sentinel."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        config: Config | None = None,
        pipeline: EventPipeline | None = None,
        sender: EventTransport | None = None,
        session_manager: SessionManager | None = None,
        trace_manager: TraceManager | None = None,
    ) -> None:
        """Initialize the Sentinel client and create a capture session.

        Args:
            api_key: API key for authenticating with the AI Sentinel backend.
            config: Optional explicit SDK configuration. When provided,
                ``api_key`` must not also be passed as a separate argument.
            pipeline: Optional event pipeline for dependency injection.
            sender: Optional event transport used when building the default
                pipeline. Ignored when ``pipeline`` is provided.
            session_manager: Optional session manager for dependency injection.
            trace_manager: Optional trace manager for dependency injection.

        Raises:
            ConfigurationError: If configuration is invalid or conflicting.
        """
        if config is not None and api_key is not None:
            raise ConfigurationError(
                "Pass either api_key or config, not both."
            )

        self._config = config or Config(api_key=api_key)
        self._config.validate()
        configure_logging(level=self._config.log_level)

        self._session_manager = session_manager or SessionManager()
        self._trace_manager = trace_manager or TraceManager()
        self._pipeline = pipeline or create_default_pipeline(self._config, sender)

        logger.info("SDK initialized endpoint_url=%s", self._config.endpoint_url)
        if self._config.verbose:
            print("SDK initialized.")

        self._session = self._create_session()

    @property
    def session(self) -> Session:
        """Return the active capture session."""
        return self._session

    @property
    def config(self) -> Config:
        """Return the active SDK configuration."""
        return self._config

    @property
    def pipeline(self) -> EventPipeline:
        """Return the event pipeline used for capture operations."""
        return self._pipeline

    def capture(
        self,
        prompt: str,
        response: str,
        framework: str = "custom",
        metadata: dict[str, Any] | None = None,
    ) -> Event:
        """Capture a prompt/response interaction as a structured event.

        The capture flows through the event pipeline::

            capture() -> Pipeline -> Validators -> Processors -> Sender

        Args:
            prompt: Input prompt sent to the model or agent.
            response: Output returned by the model or agent.
            framework: Name of the AI framework or integration source.
            metadata: Optional additional context for the event.

        Returns:
            The structured :class:`Event` that was captured and delivered.

        Raises:
            ValidationError: If required capture fields are invalid.
        """
        trace = self._trace_manager.start_span()
        context = EventContext(
            prompt=prompt,
            response=response,
            framework=framework,
            metadata=dict(metadata or {}),
            session_id=self._session.session_id,
            trace_id=trace.trace_id,
            span_id=trace.span_id,
        )

        logger.debug(
            "Capture requested session_id=%s trace_id=%s span_id=%s framework=%s",
            context.session_id,
            context.trace_id,
            context.span_id,
            context.framework,
        )
        return self._pipeline.execute(context)

    def _create_session(self) -> Session:
        """Create a new session and emit lifecycle output when verbose."""
        session = self._session_manager.create_session()
        logger.info("Session created session_id=%s", session.session_id)
        if self._config.verbose:
            print("Session created.")
        return session

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return (
            f"Sentinel(session_id={self._session.session_id!r}, "
            f"endpoint_url={self._config.endpoint_url!r})"
        )
