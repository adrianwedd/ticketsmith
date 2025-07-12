from __future__ import annotations

"""Wrapper functions for LLM API calls with cost tracking."""

from typing import Any, Dict, List

import openai
import structlog

from .metrics import record_token_usage, record_api_cost

logger = structlog.get_logger()


def chat_completion_with_tracking(
    *, model: str, messages: List[Dict[str, str]], **kwargs: Any
) -> Dict[str, Any]:
    """Call ``openai.ChatCompletion.create`` and record cost metrics.

    Args:
        model: Model name for the request.
        messages: Chat messages to send.
        **kwargs: Additional parameters passed to the OpenAI client.

    Returns:
        Raw OpenAI API response.
    """

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        **kwargs,
    )
    usage = response.get("usage", {})
    record_token_usage(usage)
    cost = record_api_cost(model=model, usage=usage)
    logger.info(
        "openai_request",
        model=model,
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        cost_usd=cost,
    )
    return response
