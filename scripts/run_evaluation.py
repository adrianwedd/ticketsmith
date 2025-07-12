"""Run LLM-judge evaluation across the dataset."""

from __future__ import annotations

import argparse
import json

from ticketsmith.evaluation import evaluate_from_files, evaluate_rag_from_files


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Evaluate agent outputs")
    parser.add_argument("dataset", help="Path to evaluation dataset JSON")
    parser.add_argument("outputs", help="Path to JSON file of agent outputs")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model name")
    parser.add_argument(
        "--report",
        default="report.json",
        help="Output report file",
    )
    parser.add_argument(
        "--rag",
        action="store_true",
        help=(
            "Run RAG triad evaluation (context relevance, groundedness, "
            "answer relevance)"
        ),
    )
    args = parser.parse_args()

    if args.rag:
        scores = evaluate_rag_from_files(
            args.dataset,
            args.outputs,
            model=args.model,
        )
    else:
        scores = evaluate_from_files(
            args.dataset,
            args.outputs,
            model=args.model,
        )
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    print(json.dumps(scores, indent=2))


if __name__ == "__main__":
    main()
