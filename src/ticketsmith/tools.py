from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable
import inspect

from pydantic import BaseModel, ValidationError, create_model


@dataclass
class Tool:
    """Encapsulate a callable with a Pydantic argument schema."""

    name: str
    description: str
    schema: type[BaseModel]
    func: Callable[..., Any]

    def __call__(self, **kwargs: Any) -> Any:
        """Validate arguments and execute the underlying function."""
        try:
            data = self.schema(**kwargs)
        except ValidationError as exc:
            raise ValueError(
                f"Invalid arguments for tool '{self.name}': {exc}"
            ) from exc
        return self.func(**data.model_dump())


def tool(name: str, description: str) -> Callable[[Callable[..., Any]], Tool]:
    """Decorator to convert a function into a :class:`Tool`."""

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
        return Tool(name=name, description=description, schema=schema, func=fn)

    return decorator


class ToolDispatcher:
    """Execute tools by name with argument validation."""

    def __init__(self, tools: Iterable[Tool]) -> None:
        self._tools: Dict[str, Tool] = {t.name: t for t in tools}

    def dispatch(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        return self._tools[name](**kwargs)

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list(self) -> Dict[str, Tool]:
        return dict(self._tools)
