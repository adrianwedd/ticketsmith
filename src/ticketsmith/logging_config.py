import logging

import structlog
from opentelemetry.trace import get_current_span


def add_trace_ids(_, __, event_dict):
    span = get_current_span()
    if span:
        span_ctx = span.get_span_context()
        if span_ctx:
            event_dict["trace_id"] = format(span_ctx.trace_id, "032x")
            event_dict["span_id"] = format(span_ctx.span_id, "016x")
    return event_dict


def configure_logging() -> None:
    """Configure structlog for JSON output with trace IDs."""
    logging.basicConfig(level=logging.INFO)
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            add_trace_ids,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
