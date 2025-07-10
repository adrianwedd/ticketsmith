# TICKETSMITH

AI-powered Jira + Confluence automation platform.

See [Project Charter](PROJECT_CHARTER.md) for objectives, use cases, and success metrics.

For a high-level architectural overview, see [Architecture Blueprint](docs/ARCHITECTURE_BLUEPRINT.md).
See [Core Agent Loop](docs/CORE_AGENT_LOOP.md) for implementation details of the ReAct loop.
See [LLM Model Selection](docs/LLM_MODEL_SELECTION.md) for the selected models and Confluence matrix.

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
