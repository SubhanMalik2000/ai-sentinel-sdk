"""
Event pipeline for the AI Sentinel SDK.

Orchestrates the validator, processor, and sender stages for every captured
event using an extensible, event-driven architecture.
"""

from ai_sentinel.pipeline.pipeline import EventPipeline, create_default_pipeline

__all__ = [
    "EventPipeline",
    "create_default_pipeline",
]
