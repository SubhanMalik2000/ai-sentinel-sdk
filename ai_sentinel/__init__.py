"""
AI Sentinel SDK package entry point.

This module exposes the public API surface of the SDK. Consumers should import
from ``ai_sentinel`` rather than reaching into internal submodules directly.
"""

from ai_sentinel.client import Sentinel
from ai_sentinel.config import Config
from ai_sentinel.events import Event, EventContext
from ai_sentinel.exceptions import (
    AuthenticationError,
    ConfigurationError,
    SentinelError,
    TransportError,
    ValidationError,
)
from ai_sentinel.instrumentation import (
    Session,
    SessionManager,
    TraceContext,
    TraceManager,
    observe,
    trace,
)
from ai_sentinel.pipeline import EventPipeline, create_default_pipeline

__all__ = [
    "AuthenticationError",
    "Config",
    "ConfigurationError",
    "Event",
    "EventContext",
    "EventPipeline",
    "Sentinel",
    "SentinelError",
    "Session",
    "SessionManager",
    "TraceContext",
    "TraceManager",
    "TransportError",
    "ValidationError",
    "create_default_pipeline",
    "observe",
    "trace",
]
__version__ = "0.0.2"
