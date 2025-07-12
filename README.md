# TICKETSMITH

AI-powered Jira + Confluence automation platform.

See [Project Charter](PROJECT_CHARTER.md) for objectives, use cases, and success metrics.

For a high-level architectural overview, see [Architecture Blueprint](docs/ARCHITECTURE_BLUEPRINT.md).
See [Core Agent Loop](docs/CORE_AGENT_LOOP.md) for implementation details of the ReAct loop.
See [LLM Model Selection](docs/LLM_MODEL_SELECTION.md) for the selected models and Confluence matrix.
For details on Atlassian API usage and authentication, see [Atlassian Integration](docs/ATLASSIAN_INTEGRATION.md).
See [RAG Architecture](docs/RAG_ARCHITECTURE.md) for the ingestion and retrieval pipeline.

## Self-Hosted Inference Server

The project ships with a containerized vLLM server that exposes an
OpenAI-compatible API. To run it locally you need an NVIDIA GPU with
Docker configured for GPU access.

Set the model repository and an API key:

```bash
export VLLM_MODEL="meta-llama/Llama-3-8B-Instruct"
export INFERENCE_API_KEY="your-secret-key"
docker compose up inference
```

Requests must include `Authorization: Bearer <API key>` to access the
`/v1/chat/completions` endpoint.

Benchmark results for tuning the vLLM server are available in
[vLLM Benchmark Results](docs/VLLM_BENCHMARKS.md).

For guidance on selecting a GPU-enabled hosting provider and configuring the
production environment, see
[Production Hosting Platform](docs/PRODUCTION_HOSTING.md).

### Local `llama-cpp-python` Inference

Developers can run quantized models directly on their machines for quick
experimentation. See [Local Inference with llama-cpp-python](docs/LOCAL_INFERENCE.md)
for installation instructions and a sample script.
