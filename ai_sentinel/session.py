"""
Session management compatibility module.

Re-exports session types from the instrumentation layer so existing imports
from ``ai_sentinel.session`` continue to work.
"""

from ai_sentinel.instrumentation.session import Session, SessionManager

__all__ = [
    "Session",
    "SessionManager",
]
