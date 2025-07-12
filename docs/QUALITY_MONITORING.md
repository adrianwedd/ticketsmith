# Quality Monitoring

This document describes how evaluation scores produced by the LLM judge are exported to Prometheus and visualized in Grafana.

## Prometheus Metrics

The evaluation framework publishes a gauge metric `ticketsmith_evaluation_score` with a `metric` label for each score such as `avg_relevance` and `avg_groundedness`. The metrics server can be started with `start_metrics_server()` and will expose these values at `/metrics`.

## Grafana Dashboards

Configure Prometheus as a data source in Grafana and create panels for the evaluation metric. Example query:

```
ticketsmith_evaluation_score{metric="avg_relevance"}
```

Add alert rules to notify the team when scores drop below acceptable thresholds, e.g. relevance < 3.0. This enables rapid detection of regressions in model quality.
