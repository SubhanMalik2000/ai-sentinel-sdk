"""
Shared utility helpers for the AI Sentinel SDK.

Contains small, stateless helper functions used across client, sender,
and event modules. Keep functions focused and side-effect free.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def generate_uuid() -> str:
    """Generate a unique identifier string.

    Returns:
        A new UUID4 string suitable for event and session identifiers.
    """
    return str(uuid4())


def utc_now() -> datetime:
    """Return the current UTC timestamp.

    Returns:
        Timezone-aware datetime in UTC.
    """
    return datetime.now(timezone.utc)
