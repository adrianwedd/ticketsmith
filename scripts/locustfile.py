"""Locust load test script for the inference API."""

from __future__ import annotations

import os
from locust import HttpUser, task, between

API_KEY = os.getenv("INFERENCE_API_KEY", "test-key")
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")


class InferenceUser(HttpUser):
    """User that sends chat completions requests."""

    wait_time = between(0.5, 2.0)

    @task
    def chat_completion(self) -> None:
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": "Hello"}],
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}
        self.client.post("/v1/chat/completions", json=payload, headers=headers)
