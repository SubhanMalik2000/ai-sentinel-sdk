"""
Basic usage example for the AI Sentinel SDK.

Demonstrates client initialization and event capture. Run from the project root:

    python examples/basic_usage.py
"""

from ai_sentinel import Sentinel

client = Sentinel(api_key="sk_test")

client.capture(
    prompt="Hello",
    response="Hi!",
)
