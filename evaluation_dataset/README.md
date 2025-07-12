# Evaluation Dataset

This directory contains the curated evaluation dataset used for end-to-end agent tests. Each entry in `dataset.json` includes:

- `id`: Unique numeric identifier.
- `prompt`: Input question or instruction.
- `expected_output`: The ideal answer or action produced by the agent.
- `context`: Documents or other information the agent should rely on.

Update the file whenever new examples are added. Changes should be committed to version control so tests always use the latest dataset.
