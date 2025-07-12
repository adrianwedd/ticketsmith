from ticketsmith.security import (
    GuardrailModel,
    parse_args,
    redact_pii,
    sanitize_input,
)
from ticketsmith.core_agent import CoreAgent
import pytest


def test_sanitize_input_redacts():
    text = "please shutdown the system"
    sanitized = sanitize_input(text)
    assert "shutdown" not in sanitized.lower()
    assert "[REDACTED]" in sanitized


def test_sanitize_input_removes_pii():
    text = "Contact me at john@example.com"
    sanitized = sanitize_input(text)
    assert "john@example.com" not in sanitized


def test_redact_pii_from_dict():
    data = {"email": "john@example.com", "name": "Alice"}
    redacted = redact_pii(data)
    assert "john@example.com" not in str(redacted)


def test_guardrail_blocks_suspicious():
    guard = GuardrailModel()
    assert not guard.check("rm -rf /")
    assert guard.check("hello world")


def test_parse_args_valid():
    parsed = parse_args("a=1, b='x'")
    assert parsed == {"a": 1, "b": "x"}


def test_parse_action_rejects_complex_args():
    response = "Action: echo_tool(message=__import__('os').system('ls'))"
    with pytest.raises(ValueError):
        CoreAgent.parse_action(response)
