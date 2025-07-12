from __future__ import annotations

import json
from typing import Dict, Iterable, List, Tuple

import openai

JUDGE_PROMPT = (
    "You are a strict judge for AI assistants. "
    "Score the candidate's answer on a scale of 1-5 for both relevance "
    "and coherence. "
    "Relevance measures how well the answer addresses the user's question. "
    "Coherence measures how logically consistent and well-structured the "
    "answer is. "
    "Respond in JSON with keys 'relevance', 'coherence', and 'rationale'."
)


def score_answer(
    question: str,
    candidate: str,
    truth: str,
    model: str = "gpt-4o",
) -> Dict[str, str | int]:
    """Score a candidate answer with an LLM judge."""
    messages = [
        {"role": "system", "content": JUDGE_PROMPT},
        {
            "role": "user",
            "content": (
                f"Question: {question}\n"
                f"Candidate answer: {candidate}\n"
                f"Ground truth: {truth}"
            ),
        },
    ]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    content = response["choices"][0]["message"]["content"]
    return json.loads(content)


def evaluate_dataset(
    dataset: Iterable[Tuple[str, str, str]],
    model: str = "gpt-4o",
) -> List[Dict[str, str | int]]:
    """Run evaluation on an iterable of question, candidate, truth tuples."""
    results: List[Dict[str, str | int]] = []
    for question, candidate, truth in dataset:
        results.append(score_answer(question, candidate, truth, model=model))
    return results


def aggregate_scores(
    results: Iterable[Dict[str, int | str]],
) -> Dict[str, float]:
    """Compute average relevance and coherence from results."""
    relevance = [r.get("relevance", 0) for r in results]
    coherence = [r.get("coherence", 0) for r in results]
    avg_rel = sum(relevance) / len(relevance) if relevance else 0.0
    avg_coh = sum(coherence) / len(coherence) if coherence else 0.0
    return {"avg_relevance": avg_rel, "avg_coherence": avg_coh}


def evaluate_from_files(
    dataset_path: str,
    outputs_path: str,
    model: str = "gpt-4o",
) -> Dict[str, float]:
    """Evaluate agent outputs loaded from files and aggregate scores."""
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    with open(outputs_path, "r", encoding="utf-8") as f:
        outputs = {int(k): v for k, v in json.load(f).items()}

    triples = [
        (item["prompt"], outputs[item["id"]], item["expected_output"])
        for item in dataset
        if item["id"] in outputs
    ]
    results = evaluate_dataset(triples, model=model)
    return aggregate_scores(results)
