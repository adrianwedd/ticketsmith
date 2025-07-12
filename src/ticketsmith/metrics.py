from __future__ import annotations

"""Prometheus metrics for Ticketsmith."""

from typing import Any, Dict
import os
import structlog

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

# Counter to track cost of API calls in USD
API_COST = Counter(
    "ticketsmith_cost_usd_total",
    "Total cost of LLM API calls in USD",
    ["model"],
)

# Pricing per 1K tokens for supported models
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4o": {"prompt": 0.005, "completion": 0.015},
    "gpt-4o-mini": {"prompt": 0.0005, "completion": 0.0015},
}

logger = structlog.get_logger()

_BUDGET_THRESHOLD = float(os.getenv("LLM_BUDGET_USD", "0") or 0)
_cumulative_cost = 0.0


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


def calculate_cost(model: str, usage: Dict[str, Any]) -> float:
    """Calculate request cost in USD based on token usage."""
    prices = MODEL_PRICING.get(model)
    if not prices:
        return 0.0
    prompt_tokens = int(usage.get("prompt_tokens", 0))
    completion_tokens = int(usage.get("completion_tokens", 0))
    return (prompt_tokens / 1000) * prices["prompt"] + (
        completion_tokens / 1000
    ) * prices["completion"]


def record_api_cost(model: str, usage: Dict[str, Any]) -> float:
    """Record API cost metric and emit budget warnings."""
    global _cumulative_cost
    cost = calculate_cost(model, usage)
    API_COST.labels(model=model).inc(cost)
    _cumulative_cost += cost
    if _BUDGET_THRESHOLD and _cumulative_cost > _BUDGET_THRESHOLD:
        logger.warning(
            "budget_exceeded",
            cost=_cumulative_cost,
            budget=_BUDGET_THRESHOLD,
        )
    return cost
