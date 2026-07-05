"""
Event pipeline for the AI Sentinel SDK.

Orchestrates the validator, processor, and sender stages for every captured
event using an extensible, event-driven architecture.
"""

from __future__ import annotations

from collections.abc import Sequence

from ai_sentinel.config import Config
from ai_sentinel.events import Event, EventContext
from ai_sentinel.logging_config import get_logger
from ai_sentinel.processors.base import Processor
from ai_sentinel.processors.enrichment import EventEnrichmentProcessor
from ai_sentinel.sender import EventSender, EventTransport
from ai_sentinel.validators.base import Validator
from ai_sentinel.validators.capture import CaptureInputValidator

logger = get_logger("pipeline")


class EventPipeline:
    """Executes captured events through validation, processing, and delivery.

    Each stage has a single responsibility and can be extended or replaced
    independently to support future framework integrations.
    """

    def __init__(
        self,
        validators: Sequence[Validator],
        processors: Sequence[Processor],
        sender: EventTransport,
    ) -> None:
        """Initialize the event pipeline.

        Args:
            validators: Ordered validation steps applied before processing.
            processors: Ordered transformation steps applied before processing.
            sender: Transport responsible for delivering finalized events.
        """
        self._validators = list(validators)
        self._processors = list(processors)
        self._sender = sender

    @property
    def validators(self) -> tuple[Validator, ...]:
        """Return the configured validator chain."""
        return tuple(self._validators)

    @property
    def processors(self) -> tuple[Processor, ...]:
        """Return the configured processor chain."""
        return tuple(self._processors)

    def execute(self, context: EventContext) -> Event:
        """Run a capture context through the full pipeline.

        Flow::

            Validator(s) -> Processor(s) -> Sender

        Args:
            context: Capture data including instrumentation identifiers.

        Returns:
            The finalized :class:`Event` that was delivered.

        Raises:
            ValidationError: If any validator rejects the context.
            ValueError: If processors fail to produce a materializable context.
        """
        logger.info(
            "Pipeline started session_id=%s trace_id=%s span_id=%s",
            context.session_id,
            context.trace_id,
            context.span_id,
        )

        for validator in self._validators:
            validator.validate(context)

        current = context
        for processor in self._processors:
            current = processor.process(current)

        event = current.to_event()
        self._sender.send(event)

        logger.info(
            "Pipeline completed event_id=%s session_id=%s trace_id=%s span_id=%s",
            event.event_id,
            event.session_id,
            event.trace_id,
            event.span_id,
        )
        return event


def create_default_pipeline(
    config: Config,
    sender: EventTransport | None = None,
) -> EventPipeline:
    """Build the default validator-processor-sender pipeline.

    Args:
        config: SDK configuration used to construct the sender when one is
            not provided explicitly.
        sender: Optional transport override for dependency injection.

    Returns:
        A fully configured :class:`EventPipeline` instance.
    """
    transport = sender or EventSender(config)
    return EventPipeline(
        validators=[CaptureInputValidator()],
        processors=[EventEnrichmentProcessor()],
        sender=transport,
    )
