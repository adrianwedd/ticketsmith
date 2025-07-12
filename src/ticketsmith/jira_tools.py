from __future__ import annotations

from requests import RequestException

import structlog

from .tools import tool
from .atlassian_auth import get_jira_client

logger = structlog.get_logger(__name__)

CREATE_DESC = (
    "Create a Jira issue. Provide project key, summary, "
    "description, and issue type."  # noqa: E501
)

TRANSITION_DESC = (
    "Transition a Jira issue to the given status name if a transition exists."
)


@tool(
    name="create_jira_issue",
    description=CREATE_DESC,
)
def create_jira_issue(
    project_key: str, summary: str, description: str, issue_type: str
) -> str:
    """Create a Jira issue and return the new issue key."""
    jira = get_jira_client()
    logger.info("create_jira_issue", project_key=project_key, summary=summary)
    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "description": description,
        "issuetype": {"name": issue_type},
    }
    try:
        issue = jira.issue_create(fields)
        return issue.get("key") or ""
    except RequestException as exc:
        raise RuntimeError(f"Failed to create issue: {exc}") from exc


@tool(
    name="add_jira_comment",
    description="Add a comment to an existing Jira issue.",
)
def add_jira_comment(issue_key: str, comment: str) -> str:
    """Add a comment to a Jira issue."""
    jira = get_jira_client()
    logger.info("add_jira_comment", issue_key=issue_key)
    try:
        jira.issue_add_comment(issue_key, comment)
        return "comment added"
    except RequestException as exc:
        raise RuntimeError(f"Failed to add comment: {exc}") from exc


@tool(
    name="assign_jira_user",
    description="Assign a Jira issue to a user by accountId.",
)
def assign_jira_user(issue_key: str, account_id: str) -> str:
    """Assign a Jira issue to a user."""
    jira = get_jira_client()
    logger.info("assign_jira_user", issue_key=issue_key, account_id=account_id)
    try:
        jira.assign_issue(issue_key, account_id=account_id)
        return "issue assigned"
    except RequestException as exc:
        raise RuntimeError(f"Failed to assign user: {exc}") from exc


@tool(
    name="transition_jira_issue",
    description=TRANSITION_DESC,
)
def transition_jira_issue(issue_key: str, status_name: str) -> str:
    """Transition a Jira issue to the specified status."""
    jira = get_jira_client()
    logger.info(
        "transition_jira_issue",
        issue_key=issue_key,
        status=status_name,
    )
    try:
        transition_id = jira.get_transition_id_to_status_name(
            issue_key,
            status_name,
        )
        if transition_id is None:
            msg_template = (
                "No transition to status '{status}' for issue '{key}'"  # noqa: E501
            )
            msg = msg_template.format(status=status_name, key=issue_key)
            raise RuntimeError(msg)
        jira.issue_transition(issue_key, status_name)
        return f"issue transitioned to {status_name}"
    except RequestException as exc:
        raise RuntimeError(f"Failed to transition issue: {exc}") from exc
