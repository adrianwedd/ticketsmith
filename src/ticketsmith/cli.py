from __future__ import annotations

import click

from .logging_config import configure_logging
from .tracing import configure_tracing
from .metrics import start_metrics_server

from .core_agent import CoreAgent
from .tools import ToolDispatcher, tool


@tool(name="echo_tool", description="Return the given message.")
def echo_tool(message: str) -> str:
    """Return the given message."""
    return message


def dummy_llm(prompt: str) -> str:
    """Simple LLM stub that always returns a predefined action."""
    return "Thought: echoing message\nAction: echo_tool(message='Hello')"


@click.command()
@click.argument("text")
def main(text: str) -> None:
    """Run the core agent once with the provided text."""
    configure_logging()
    configure_tracing()
    start_metrics_server()
    dispatcher = ToolDispatcher([echo_tool])
    agent = CoreAgent(dummy_llm, dispatcher)
    result = agent.run(text)
    click.echo(result)


if __name__ == "__main__":
    main()
