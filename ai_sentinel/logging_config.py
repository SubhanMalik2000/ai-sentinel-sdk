"""
Structured logging configuration for the AI Sentinel SDK.

Centralizes logger creation and optional handler setup so every module uses
consistent, namespaced log records via the standard library ``logging`` module.
"""

from __future__ import annotations

import logging
import sys
from typing import Final

LOGGER_ROOT: Final[str] = "ai_sentinel"
_DEFAULT_CONFIGURED: bool = False


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a namespaced logger for SDK components.

    Args:
        name: Optional submodule suffix (for example ``"pipeline"`` or
            ``"validators.capture"``). When omitted, returns the root SDK
            logger.

    Returns:
        A configured :class:`logging.Logger` instance under the ``ai_sentinel``
        namespace.
    """
    if name:
        return logging.getLogger(f"{LOGGER_ROOT}.{name}")
    return logging.getLogger(LOGGER_ROOT)


def configure_logging(
    *,
    level: int = logging.INFO,
    stream: object | None = None,
    force: bool = False,
) -> None:
    """Configure structured logging for the SDK.

    Installs a single stream handler on the root SDK logger with a consistent
    format suitable for production log aggregation. Safe to call multiple
    times; subsequent calls are no-ops unless ``force`` is ``True``.

    Args:
        level: Logging level for the SDK root logger.
        stream: Output stream for log records. Defaults to ``sys.stderr``.
        force: When ``True``, replace any existing handler configuration.
    """
    global _DEFAULT_CONFIGURED

    logger = get_logger()
    if _DEFAULT_CONFIGURED and not force:
        return

    if force or not logger.handlers:
        logger.handlers.clear()
        handler = logging.StreamHandler(stream or sys.stderr)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
        logger.addHandler(handler)

    logger.setLevel(level)
    logger.propagate = False
    _DEFAULT_CONFIGURED = True
