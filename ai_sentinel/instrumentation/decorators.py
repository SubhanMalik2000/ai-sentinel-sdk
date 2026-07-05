"""
Instrumentation decorator placeholders for the AI Sentinel SDK.

Provides no-op decorators that preserve call semantics today while reserving
extension points for Sprint 4 framework integrations.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeVar

from ai_sentinel.logging_config import get_logger

logger = get_logger("instrumentation.decorators")

F = TypeVar("F", bound=Callable[..., Any])


def trace(name: str | None = None) -> Callable[[F], F]:
    """Placeholder decorator for future trace instrumentation.

    Args:
        name: Optional logical name for the traced callable. Reserved for
            future use; currently ignored.

    Returns:
        A decorator that wraps the target callable without altering behavior.
    """

    def decorator(func: F) -> F:
        trace_name = name or func.__qualname__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug("trace placeholder invoked name=%s", trace_name)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def observe(name: str | None = None) -> Callable[[F], F]:
    """Placeholder decorator for future observation instrumentation.

    Args:
        name: Optional logical name for the observed callable. Reserved for
            future use; currently ignored.

    Returns:
        A decorator that wraps the target callable without altering behavior.
    """

    def decorator(func: F) -> F:
        observe_name = name or func.__qualname__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug("observe placeholder invoked name=%s", observe_name)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
