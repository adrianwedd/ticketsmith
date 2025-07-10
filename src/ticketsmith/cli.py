from __future__ import annotations

import click

from .core_agent import CoreAgent


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
    agent = CoreAgent(dummy_llm, {"echo_tool": echo_tool})
    result = agent.run(text)
    click.echo(result)


if __name__ == "__main__":
    main()
