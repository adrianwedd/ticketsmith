#!/bin/bash

if [ -z "$INFERENCE_API_KEY" ]; then
  echo "INFERENCE_API_KEY not set" >&2
  exit 1
fi

exec python3 -m vllm.entrypoints.openai.api_server \
  --model "$VLLM_MODEL" \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key "$INFERENCE_API_KEY"

