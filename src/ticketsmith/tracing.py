"""Configure OpenTelemetry tracing and instrumentation."""

from __future__ import annotations

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)


def configure_tracing(service_name: str = "ticketsmith") -> None:
    """Configure OpenTelemetry tracing and instrument common libraries."""
    provider = TracerProvider(
        resource=Resource.create({"service.name": service_name}),
    )
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    RequestsInstrumentor().instrument()


def instrument_flask_app(app) -> None:
    """Instrument a Flask application for tracing."""
    FlaskInstrumentor().instrument_app(app)
