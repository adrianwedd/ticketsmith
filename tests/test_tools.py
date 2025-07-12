from ticketsmith.tools import ToolDispatcher, tool
import pytest


@tool(name="add", description="Add two integers together.", scope="math:add")
def add(a: int, b: int) -> int:
    return a + b


def test_dispatcher_executes_tool():
    dispatcher = ToolDispatcher([add])
    assert dispatcher.dispatch("add", a=2, b=3) == 5


def test_dispatcher_validates_arguments():
    dispatcher = ToolDispatcher([add])
    with pytest.raises(ValueError):
        dispatcher.dispatch("add", a="x", b=1)
