from ticketsmith.evaluation import aggregate_rag_scores


def test_aggregate_rag_scores():
    results = [
        {"context_relevance": 5, "answer_relevance": 4, "groundedness": 3},
        {"context_relevance": 3, "answer_relevance": 5, "groundedness": 4},
    ]
    agg = aggregate_rag_scores(results)
    assert agg["avg_context_relevance"] == 4.0
    assert agg["avg_answer_relevance"] == 4.5
    assert agg["avg_groundedness"] == 3.5
