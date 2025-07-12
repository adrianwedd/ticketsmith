"""Human-in-the-loop approval utilities."""

from __future__ import annotations

import os
import time
from typing import Dict

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackApprovalClient:
    """Request approval for high-risk actions via Slack."""

    def __init__(
        self,
        token: str | None = None,
        channel: str | None = None,
        timeout: int = 300,
    ) -> None:
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        self.channel = channel or os.getenv("SLACK_APPROVAL_CHANNEL", "")
        self.timeout = timeout
        self.client = WebClient(token=self.token)

    def request_approval(self, action: str, params: Dict[str, object]) -> bool:
        """Send an approval request and poll for a response."""

        message = (
            f"Approve action `{action}` with args `{params}`? "
            "React with :thumbsup: to approve or :x: to reject."
        )
        try:
            resp = self.client.chat_postMessage(
                channel=self.channel,
                text=message,
            )
            ts = resp["ts"]
        except SlackApiError as exc:  # pragma: no cover - network
            raise RuntimeError(
                f"Failed to send Slack message: {exc.response['error']}"
            ) from exc

        end = time.time() + self.timeout
        while time.time() < end:
            time.sleep(5)
            try:
                result = self.client.reactions_get(
                    channel=self.channel,
                    timestamp=ts,
                )
                reactions = {
                    r["name"] for r in result["message"].get("reactions", [])
                }  # noqa: E501
                if "thumbsup" in reactions:
                    return True
                if "x" in reactions:
                    return False
            except SlackApiError:  # pragma: no cover - network
                pass
        return False
