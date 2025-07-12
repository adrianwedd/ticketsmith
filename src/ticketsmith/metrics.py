from __future__ import annotations

"""Prometheus metrics for Ticketsmith."""

from typing import Any, Dict

from prometheus_client import Counter, Histogram, start_http_server

# Histogram to track latency of agent requests
REQUEST_LATENCY = Histogram(
    "ticketsmith_request_latency_seconds", "Latency of agent requests"
)

# Counter to track total error count
ERROR_COUNT = Counter("ticketsmith_error_total", "Total number of errors")

# Counter to track token usage for LLM calls
TOKEN_USAGE = Counter(
    "ticketsmith_tokens_total",
    "Total tokens used",
    ["type"],
)


def start_metrics_server(port: int = 8000) -> None:
    """Start the Prometheus metrics HTTP server."""
    start_http_server(port)


def record_token_usage(usage: Dict[str, Any]) -> None:
    """Record token usage metrics.

    Args:
        usage: Response ``usage`` object with ``prompt_tokens`` and
            ``completion_tokens`` counts.
    """
    prompt_tokens = int(usage.get("prompt_tokens", 0))
    completion_tokens = int(usage.get("completion_tokens", 0))
    TOKEN_USAGE.labels(type="prompt").inc(prompt_tokens)
    TOKEN_USAGE.labels(type="completion").inc(completion_tokens)
