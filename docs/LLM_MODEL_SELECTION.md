# LLM Model Selection

A comprehensive **LLM Model Selection Matrix** is published in the project's Confluence space: <https://confluence.example.com/display/TS/LLM+Model+Selection+Matrix>.
The matrix compares GPT-4o, Claude 3, Llama 3.1, and Mistral Large across:

- Context window size
- Function calling support
- Multimodal capabilities
- Benchmark performance (MMLU, HumanEval)
- Cost per million tokens

## Decision

- **Primary model:** OpenAI GPT-4o for core reasoning and planning.
- **Specialized model:** Anthropic Claude 3 for summarization and classification tasks.

API keys for these models are provisioned and stored securely in the company's secret management system. Access is restricted to the development team.
