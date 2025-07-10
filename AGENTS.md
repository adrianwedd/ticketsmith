# Repository Guide for AI Agents

The instructions in this file apply to the entire repository.

- Use **Python 3.11** for any new scripts or modules.
- Format all Python code with `black` and lint with `flake8` before committing.
- Execute `pytest` to run the test suite if tests exist.
- Keep `requirements.txt` updated when adding dependencies.
- Document new functions with Google style docstrings.
- Summaries for pull requests must describe the change and reference any tests executed.
- Review `tasks.yaml` before starting work. Update a task's `status` to `done` in this file before committing related changes.
- Consult `BLUEPRINT.md` for architectural context and planning guidance.
- Record any new issues or opportunities for improvement by adding tasks to `tasks.yaml` using the existing schema.
- Capture important insights or workflow updates here in `AGENTS.md` so future agents can benefit from them.
- Reference relevant task IDs in commit messages for traceability.
- Maintain unique, sequential numeric IDs when adding new tasks and keep `tasks.yaml` sorted by `id`.
