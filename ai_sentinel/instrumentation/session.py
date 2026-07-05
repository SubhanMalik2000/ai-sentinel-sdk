"""
Session management for the AI Sentinel SDK instrumentation layer.

Tracks session identifiers and creation metadata for grouped event capture.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ai_sentinel.logging_config import get_logger
from ai_sentinel.utils import generate_uuid, utc_now

logger = get_logger("instrumentation.session")


@dataclass(frozen=True)
class Session:
    """Represents an active SDK capture session.

    Attributes:
        session_id: Unique identifier for the session.
        created_at: UTC timestamp when the session was created.
    """

    session_id: str
    created_at: datetime


class SessionManager:
    """Creates and manages SDK sessions."""

    def __init__(self) -> None:
        """Initialize a session manager without an active session."""
        self._current: Session | None = None

    @property
    def current(self) -> Session | None:
        """Return the active session, if one has been created."""
        return self._current

    def create_session(self) -> Session:
        """Create a new capture session and set it as the active session.

        Returns:
            A new :class:`Session` with generated identifiers and timestamps.
        """
        session = Session(session_id=generate_uuid(), created_at=utc_now())
        self._current = session
        logger.debug("Session created session_id=%s", session.session_id)
        return session

    def get_or_create_session(self) -> Session:
        """Return the active session, creating one when absent.

        Returns:
            The current or newly created :class:`Session`.
        """
        if self._current is None:
            return self.create_session()
        return self._current
