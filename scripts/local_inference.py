"""Example script for running a GGUF model locally with llama-cpp-python."""

from __future__ import annotations

from llama_cpp import Llama

MODEL_PATH = "./models/llama-3-8b-instruct.Q4_K_M.gguf"


def main() -> None:
    """Load the model and generate a short completion."""
    llm = Llama(model_path=MODEL_PATH)
    response = llm("Hello, world!", max_tokens=32)
    print(response["choices"][0]["text"].strip())


if __name__ == "__main__":
    main()
