"""
Validator contracts and exports for the AI Sentinel event pipeline.

Validators enforce preconditions on :class:`~ai_sentinel.events.EventContext`
instances before processors mutate or materialize events.
"""

from ai_sentinel.validators.base import Validator
from ai_sentinel.validators.capture import CaptureInputValidator

__all__ = [
    "CaptureInputValidator",
    "Validator",
]
