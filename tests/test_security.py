from ticketsmith.security import sanitize_input, GuardrailModel, parse_args
from ticketsmith.core_agent import CoreAgent
import pytest


def test_sanitize_input_redacts():
    text = "please shutdown the system"
    sanitized = sanitize_input(text)
    assert "shutdown" not in sanitized.lower()
    assert "[REDACTED]" in sanitized


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
