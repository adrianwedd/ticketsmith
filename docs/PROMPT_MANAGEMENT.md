# Prompt Management

Prompt templates live in `src/ticketsmith/prompts/` and are treated as version-controlled assets. Each file is named using the pattern `<name>_prompt.txt` and describes a single prompt used by the application.

Use `ticketsmith.load_prompt(name)` to fetch a template at runtime. For example, `load_prompt("system_prompt")` returns the system prompt for the core agent.

Changes to prompt files follow the same review process as code. When adding or modifying a prompt, document its purpose, expected inputs, and expected behavior in this file.
Prompt updates require standard code review to maintain consistency.
