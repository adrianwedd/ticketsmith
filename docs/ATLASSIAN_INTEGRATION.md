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
