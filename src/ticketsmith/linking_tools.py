from __future__ import annotations

import os
from typing import Dict

from .tools import tool
from .jira_tools import create_jira_issue, add_jira_comment
from .confluence_tools import create_confluence_page


LINK_DESC = (
    "Create a Jira issue and Confluence page with reciprocal links. "
    "Provide project key, summary, description, issue type, Confluence space, "
    "title, and body."
)


@tool(
    name="create_linked_issue_and_page",
    description=LINK_DESC,
    scope="link:create",
)
def create_linked_issue_and_page(
    project_key: str,
    summary: str,
    description: str,
    issue_type: str,
    space: str,
    title: str,
    body: str,
) -> Dict[str, str]:
    """Create linked Jira issue and Confluence page.

    Args:
        project_key: Jira project key.
        summary: Issue summary.
        description: Issue description.
        issue_type: Type of Jira issue (e.g., Task).
        space: Confluence space key.
        title: Title for the Confluence page.
        body: Initial page body in storage format.

    Returns:
        Dictionary with ``issue_key`` and ``page_id``.
    """

    base_url = os.environ.get("ATLASSIAN_BASE_URL", "").rstrip("/")
    if not base_url:
        raise RuntimeError("ATLASSIAN_BASE_URL is required")

    try:
        issue_key = create_jira_issue(
            project_key=project_key,
            summary=summary,
            description=description,
            issue_type=issue_type,
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to create Jira issue: {exc}") from exc

    issue_url = f"{base_url}/browse/{issue_key}"
    body_with_link = body + (
        "<p>Related Jira issue: " f"<a href='{issue_url}'>{issue_key}</a></p>"
    )

    try:
        page_id = create_confluence_page(
            space=space,
            title=title,
            body=body_with_link,
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to create Confluence page: {exc}") from exc

    page_url = f"{base_url}/wiki/spaces/{space}/pages/{page_id}"

    try:
        add_jira_comment(
            issue_key=issue_key,
            comment=f"Confluence page: {page_url}",
        )
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to comment on Jira issue: {exc}") from exc

    return {"issue_key": issue_key, "page_id": page_id}
