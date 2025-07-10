# Atlassian Integration

The project uses the [`atlassian-python-api`](https://pypi.org/project/atlassian-python-api/) library for all Jira and Confluence interactions. A shared module, `ticketsmith.atlassian_auth`, provides helper functions to create authenticated clients.

## Authentication

`atlassian-python-api` relies on basic authentication with an API token. The module reads the following environment variables:

- `ATLASSIAN_BASE_URL` – base URL of your Atlassian cloud instance
- `ATLASSIAN_USERNAME` – email address associated with the API token
- `ATLASSIAN_API_TOKEN` – API token generated in your Atlassian account

Example usage:

```python
from ticketsmith.atlassian_auth import get_jira_client, get_confluence_client

jira = get_jira_client()
confluence = get_confluence_client()
```

Ensure these values are stored securely, for example in a secrets manager when running in production.

## Jira Tools

Several helper tools wrap common Jira operations. They use the shared
authentication module and provide descriptive prompts so the agent can
use them effectively.

```python
from ticketsmith.jira_tools import (
    create_jira_issue,
    add_jira_comment,
    assign_jira_user,
    transition_jira_issue,
)

# create an issue and then transition it
key = create_jira_issue(
    project_key="PROJ",
    summary="Example",
    description="Example issue",
    issue_type="Task",
)
add_jira_comment(key, "Created via tool")
assign_jira_user(key, account_id="12345")
transition_jira_issue(key, "Done")
```
