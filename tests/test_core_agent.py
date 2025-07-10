from ticketsmith.core_agent import CoreAgent
from ticketsmith.tools import ToolDispatcher, tool


def test_single_loop():
    def llm(_prompt: str) -> str:
        return "Thought: say hello\nAction: echo_tool(message='hi')"

    @tool(name="echo_tool", description="Return the given message.")
    def echo_tool(message: str) -> str:
        return message

    dispatcher = ToolDispatcher([echo_tool])
    agent = CoreAgent(llm, dispatcher)
    result = agent.run("test")
    history = result.get("history")
    assert history is not None
    assert history[0]["observation"] == "hi"
    assert history[0]["action"]["tool"] == "echo_tool"
    assert history[0]["action"]["args"] == {"message": "hi"}
