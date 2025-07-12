# Performance and Load Testing

This document outlines service level objectives (SLOs) and provides instructions for running the load tests.

## Latency SLOs

- **p50 latency**: responses should be under **1 second**.
- **p95 latency**: responses should be under **3 seconds**.

These SLOs apply to the `/v1/chat/completions` endpoint exposed by the vLLM inference service.

## Simulating Load

We use [Locust](https://locust.io/) to generate traffic. Install dependencies from `requirements.txt` and run:

```bash
locust -f scripts/locustfile.py --headless -u 20 -r 5 -t 1m
```

- `-u` specifies the number of concurrent users.
- `-r` controls hatch rate (users spawned per second).
- `-t` sets test duration.

## Metrics Collection

The test records request latency and failure rates. After the run, Locust prints aggregated statistics including average latency, percentile latencies and error counts. Review these metrics against the SLOs to identify bottlenecks. High latencies or frequent failures indicate areas requiring optimization.

