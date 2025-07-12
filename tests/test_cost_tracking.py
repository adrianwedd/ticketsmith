from ticketsmith.cost_tracking import chat_completion_with_tracking
from ticketsmith.metrics import calculate_cost, API_COST, TOKEN_USAGE
import openai


def test_calculate_cost():
    usage = {"prompt_tokens": 1000, "completion_tokens": 1000}
    cost = calculate_cost("gpt-4o", usage)
    assert cost == 0.005 + 0.015


def test_chat_completion_with_tracking(monkeypatch):
    def fake_create(*args, **kwargs):
        return {
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        }

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    TOKEN_USAGE.labels(type="prompt")._value.set(0)
    TOKEN_USAGE.labels(type="completion")._value.set(0)
    API_COST.labels(model="gpt-4o")._value.set(0)

    resp = chat_completion_with_tracking(
        model="gpt-4o", messages=[{"role": "user", "content": "hi"}]
    )
    assert resp["choices"][0]["message"]["content"] == "ok"
    assert TOKEN_USAGE.labels(type="prompt")._value.get() == 10
    assert API_COST.labels(model="gpt-4o")._value.get() > 0
