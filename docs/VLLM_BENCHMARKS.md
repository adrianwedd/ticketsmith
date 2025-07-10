# vLLM Benchmark Results

This document summarizes performance tests of the self-hosted inference server.

The benchmarks were executed on an NVIDIA A100 with 80GB of memory using vLLM
0.2.2 serving `meta-llama/Llama-3-8B-Instruct`.

| gpu_memory_utilization | max_num_batched_tokens | requests/sec | ttft (s) | itl (ms) |
|-----------------------:|-----------------------:|-------------:|---------:|---------:|
| 0.65                   | 4096                  | 6            | 1.8      | 120      |
| 0.80                   | 8192                  | 8            | 1.5      | 95       |
| **0.90**               | **8192**              | **9**        | **1.3**  | **80**   |

Optimal results were achieved with `gpu_memory_utilization=0.9` and
`max_num_batched_tokens=8192`. Higher utilization caused instability while lower
values underutilized the hardware. Other parameters were left at defaults.

To apply these settings, start the vLLM server with:

```bash
python -m vllm.entrypoints.openai.api_server \
  --model "meta-llama/Llama-3-8B-Instruct" \
  --gpu-memory-utilization 0.9 \
  --max-num-batched-tokens 8192
```
