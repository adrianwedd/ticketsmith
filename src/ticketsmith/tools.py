from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable
import inspect
import os

from opentelemetry import trace
from pydantic import BaseModel, ValidationError, create_model

from .token_auth import (
    validate_token,
    load_token_scopes,
    InvalidTokenError,
)

tracer = trace.get_tracer(__name__)


@dataclass
class Tool:
    """Encapsulate a callable with a Pydantic argument schema."""

    name: str
    description: str
    schema: type[BaseModel]
    func: Callable[..., Any]
    scope: str

    def __call__(self, **kwargs: Any) -> Any:
        """Validate arguments and execute the underlying function."""
        try:
            data = self.schema(**kwargs)
        except ValidationError as exc:
            raise ValueError(
                f"Invalid arguments for tool '{self.name}': {exc}"
            ) from exc
        return self.func(**data.model_dump())


def tool(
    name: str, description: str, scope: str
) -> Callable[[Callable[..., Any]], Tool]:
    """Decorator to convert a function into a :class:`Tool` with a scope."""

    def decorator(fn: Callable[..., Any]) -> Tool:
        parameters: Dict[str, tuple[Any, Any]] = {}
        # fmt: off
        for param in inspect.signature(fn).parameters.values():
            annotation = (
                param.annotation
                if param.annotation is not inspect._empty
                else Any
            )
            default = (
                param.default
                if param.default is not inspect._empty
                else ...
            )
            parameters[param.name] = (annotation, default)
        # fmt: on
        schema = create_model(f"{fn.__name__.title()}Args", **parameters)
        return Tool(
            name=name,
            description=description,
            schema=schema,
            func=fn,
            scope=scope,
        )

    return decorator


class ToolDispatcher:
    """Execute tools by name with argument validation and token checks."""

    def __init__(
        self,
        tools: Iterable[Tool],
        token: str | None = None,
        approval_client: Any | None = None,
        high_risk_tools: Iterable[str] | None = None,
    ) -> None:
        self._tools: Dict[str, Tool] = {t.name: t for t in tools}
        self._token = token or os.getenv("TOOL_ACCESS_TOKEN")
        self._token_scopes = load_token_scopes()
        self._approval_client = approval_client
        self._high_risk = set(high_risk_tools or [])

    def dispatch(
        self,
        name: str,
        token: str | None = None,
        **kwargs: Any,
    ) -> Any:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        tool = self._tools[name]
        access_token = token or self._token
        if not access_token:
            raise InvalidTokenError("401 Unauthorized: missing token")
        validate_token(access_token, tool.scope, self._token_scopes)
        if name in self._high_risk and self._approval_client:
            approved = self._approval_client.request_approval(name, kwargs)
            if not approved:
                raise PermissionError(f"Action {name} was not approved")
        with tracer.start_as_current_span(
            "tool_execution",
            attributes={"tool": name},
        ):
            return tool(**kwargs)

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list(self) -> Dict[str, Tool]:
        return dict(self._tools)
