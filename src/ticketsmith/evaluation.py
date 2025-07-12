from __future__ import annotations

import json
from typing import Dict, Iterable, List, Tuple

import openai

JUDGE_PROMPT = (
    "You are a strict judge for AI assistants. "
    "Score the candidate's answer on a scale of 1-5 for relevance, coherence, "
    "and groundedness. "
    "Relevance measures how well the answer addresses the user's question. "
    "Coherence measures how logically consistent and well-structured the "
    "answer is. "
    "Groundedness measures whether each statement in the answer is supported "
    "by the provided context. If a claim is unsupported, groundedness should "
    "be low. "
    "Respond in JSON with keys 'relevance', 'coherence', 'groundedness', and "
    "'rationale'."
)

# Additional prompt for RAG-specific evaluation
RAG_JUDGE_PROMPT = (
    "You are a strict judge for RAG systems. "
    "Score the retrieved context and candidate answer on a scale of 1-5 for "
    "context relevance, answer relevance, and groundedness. "
    "Context relevance measures how well the provided context matches the "
    "user's question. Answer relevance measures how well the candidate "
    "answer addresses the question. Groundedness measures whether the "
    "answer is supported by the context. Respond in JSON with keys "
    "'context_relevance', 'answer_relevance', 'groundedness', and "
    "'rationale'."
)


def score_answer(
    question: str,
    candidate: str,
    truth: str,
    context: str | None = None,
    model: str = "gpt-4o",
) -> Dict[str, str | int]:
    """Score a candidate answer with an LLM judge.

    The judge returns relevance, coherence, and groundedness scores.
    """
    messages = [
        {"role": "system", "content": JUDGE_PROMPT},
        {
            "role": "user",
            "content": (
                f"Question: {question}\n"
                f"Candidate answer: {candidate}\n"
                f"Ground truth: {truth}\n"
                f"Context: {context or ''}"
            ),
        },
    ]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    content = response["choices"][0]["message"]["content"]
    return json.loads(content)


def score_rag_answer(
    question: str,
    candidate: str,
    retrieved_context: str,
    truth: str,
    model: str = "gpt-4o",
) -> Dict[str, str | int]:
    """Score a RAG answer with context using an LLM judge."""
    messages = [
        {"role": "system", "content": RAG_JUDGE_PROMPT},
        {
            "role": "user",
            "content": (
                f"Question: {question}\n"
                f"Retrieved context: {retrieved_context}\n"
                f"Candidate answer: {candidate}\n"
                f"Ground truth: {truth}"
            ),
        },
    ]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    content = response["choices"][0]["message"]["content"]
    return json.loads(content)


def evaluate_dataset(
    dataset: Iterable[Tuple[str, str, str, str]],
    model: str = "gpt-4o",
) -> List[Dict[str, str | int]]:
    """Run evaluation on question, candidate, truth, and context tuples."""
    results: List[Dict[str, str | int]] = []
    for question, candidate, truth, context in dataset:
        results.append(
            score_answer(
                question,
                candidate,
                truth,
                context=context,
                model=model,
            )
        )
    return results


def evaluate_rag_dataset(
    dataset: Iterable[Tuple[str, str, str, str]],
    model: str = "gpt-4o",
) -> List[Dict[str, str | int]]:
    """Run RAG evaluation on question, answer, context, and ground truth."""
    results: List[Dict[str, str | int]] = []
    for question, candidate, context, truth in dataset:
        results.append(
            score_rag_answer(
                question,
                candidate,
                context,
                truth,
                model=model,
            )
        )
    return results


def aggregate_scores(
    results: Iterable[Dict[str, int | str]],
) -> Dict[str, float]:
    """Compute average relevance, coherence, and groundedness from results."""
    relevance = [r.get("relevance", 0) for r in results]
    coherence = [r.get("coherence", 0) for r in results]
    groundedness = [r.get("groundedness", 0) for r in results]
    avg_rel = sum(relevance) / len(relevance) if relevance else 0.0
    avg_coh = sum(coherence) / len(coherence) if coherence else 0.0
    avg_ground = sum(groundedness) / len(groundedness) if groundedness else 0.0
    return {
        "avg_relevance": avg_rel,
        "avg_coherence": avg_coh,
        "avg_groundedness": avg_ground,
    }


def aggregate_rag_scores(
    results: Iterable[Dict[str, int | str]],
) -> Dict[str, float]:
    """Compute average context relevance, answer relevance, and "
    "groundedness."""
    context_rel = [r.get("context_relevance", 0) for r in results]
    answer_rel = [r.get("answer_relevance", 0) for r in results]
    grounded = [r.get("groundedness", 0) for r in results]
    avg_ctx = sum(context_rel) / len(context_rel) if context_rel else 0.0
    avg_ans = sum(answer_rel) / len(answer_rel) if answer_rel else 0.0
    avg_ground = sum(grounded) / len(grounded) if grounded else 0.0
    return {
        "avg_context_relevance": avg_ctx,
        "avg_answer_relevance": avg_ans,
        "avg_groundedness": avg_ground,
    }


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
        (
            item["prompt"],
            outputs[item["id"]],
            item["expected_output"],
            item.get("context", ""),
        )
        for item in dataset
        if item["id"] in outputs
    ]
    results = evaluate_dataset(triples, model=model)
    return aggregate_scores(results)


def evaluate_rag_from_files(
    dataset_path: str,
    outputs_path: str,
    model: str = "gpt-4o",
) -> Dict[str, float]:
    """Evaluate RAG outputs loaded from files and aggregate scores."""
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    with open(outputs_path, "r", encoding="utf-8") as f:
        outputs = {int(k): v for k, v in json.load(f).items()}

    rows = []
    for item in dataset:
        out = outputs.get(item["id"])
        if not out:
            continue
        answer = out.get("answer") if isinstance(out, dict) else out
        context = out.get("context", "") if isinstance(out, dict) else ""
        rows.append(
            (
                item["prompt"],
                answer,
                context,
                item["expected_output"],
            )
        )
    results = evaluate_rag_dataset(rows, model=model)
    return aggregate_rag_scores(results)
