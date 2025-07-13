"""Utilities for loading prompt templates."""

from __future__ import annotations

from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt template by name.

    Args:
        name: Base filename of the prompt template without extension.

    Returns:
        Contents of the prompt template.
    """
    path = PROMPT_DIR / f"{name}.txt"
    return path.read_text(encoding="utf-8")
