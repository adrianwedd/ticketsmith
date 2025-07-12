"""Utilities for interacting with Confluence."""

from __future__ import annotations

from requests import RequestException

import structlog

from .tools import tool
from .atlassian_auth import get_confluence_client

logger = structlog.get_logger(__name__)

CREATE_DESC = (
    "Create a Confluence page in the given space with the provided "
    "title and body."  # noqa: E501
)

SEARCH_DESC = (
    "Search Confluence using the siteSearch field to find relevant "
    "pages."  # noqa: E501
)

APPEND_DESC = "Append content to an existing Confluence page by ID."


@tool(
    name="create_confluence_page",
    description=CREATE_DESC,
    scope="confluence:page:create",
)
def create_confluence_page(space: str, title: str, body: str) -> str:
    """Create a Confluence page.

    Args:
        space: Confluence space key.
        title: Title of the new page.
        body: Page body content in storage format.

    Returns:
        The ID of the created page.
    """

    confluence = get_confluence_client()
    logger.info("create_confluence_page", space=space, title=title)
    try:
        page = confluence.create_page(space, title, body)
        return str(page.get("id", ""))
    except RequestException as exc:
        raise RuntimeError(f"Failed to create page: {exc}") from exc


@tool(
    name="search_confluence",
    description=SEARCH_DESC,
    scope="confluence:page:read",
)
def search_confluence(query: str) -> dict:
    """Search Confluence pages.

    Args:
        query: Query string to search for.

    Returns:
        Raw search results from the Confluence API.
    """

    confluence = get_confluence_client()
    logger.info("search_confluence", query=query)
    cql_query = f"siteSearch ~ '{query}'"
    try:
        return confluence.cql(cql_query)
    except RequestException as exc:
        raise RuntimeError(f"Failed to search Confluence: {exc}") from exc


@tool(
    name="append_to_confluence_page",
    description=APPEND_DESC,
    scope="confluence:page:update",
)
def append_to_confluence_page(page_id: str, content: str) -> str:
    """Append content to a Confluence page.

    Args:
        page_id: Identifier of the page to update.
        content: Content to append in storage format.

    Returns:
        Confirmation message when complete.
    """

    confluence = get_confluence_client()
    logger.info("append_to_confluence_page", page_id=page_id)
    try:
        confluence.append_page(page_id, content)
        return "content appended"
    except RequestException as exc:
        raise RuntimeError(f"Failed to append content: {exc}") from exc
