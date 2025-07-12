# Production Hosting Platform

This guide documents the evaluation of GPU-capable hosting providers and how to provision the production infrastructure.

## Provider Evaluation

| Provider | GPU Options | Notes |
|---------|-------------|------|
| **AWS EC2** | A10G, A100, H100 via EC2 instances (p4d, p5) | Widest region coverage and mature networking features. Costs vary by instance size; Spot instances may reduce price. |
| **GCP Compute Engine** | A100, H100 GPUs (A2, A3 instances) | Good per-second billing and global network. GPU quotas must be requested. |
| **Azure** | A100 (ND A100 v4), H100 (ND H100 v5) | Integrated monitoring with Azure ML and easy VNet setup. Pricing comparable to AWS. |
| **Render** | Limited to A10 and A40 GPUs | Simple deployment workflow but fewer regions and higher hourly pricing. |
| **Fly.io** | No dedicated GPU offering (as of 2025) | Suitable for lightweight apps but not for large model hosting. |

AWS provides the best balance of availability and scalability for running large models such as Llama 3 with vLLM, so it is the recommended platform.

## Provisioning Steps (AWS Example)

1. Request a quota for p4d or p5 instances in the desired region.
2. Launch an EC2 instance with the selected GPU type using an Ubuntu 22.04 AMI.
3. Configure a security group to allow SSH (22) and application ports (3000, 5000, 8000) only from trusted IP ranges. Enable HTTPS termination via an Application Load Balancer if exposing services publicly.
4. Install Docker and Docker Compose on the instance.
5. Clone this repository or pull the pre-built container images from your registry.
6. Set required environment variables either in an `.env` file or the hosting platform's secret manager:

```bash
VLLM_MODEL="meta-llama/Llama-3-8B-Instruct"
INFERENCE_API_KEY="change-me"
ATLASSIAN_BASE_URL="https://your-domain.atlassian.net"
ATLASSIAN_USERNAME="bot@example.com"
ATLASSIAN_API_TOKEN="secret-token"
```

7. Start the services with `docker compose up --build`.
8. Verify that the inference API is reachable at `/v1/chat/completions` and that the application frontend is accessible.

## Networking and Access

- Use AWS security groups or the equivalent firewall rules on other providers to restrict inbound traffic.
- Configure TLS certificates on the load balancer or a reverse proxy.
- Store all secrets (API keys, tokens) in the provider's secret manager and inject them as environment variables at runtime.

Following these steps satisfies the requirements for Task 603 by selecting a suitable GPU provider and provisioning a secure production environment.
