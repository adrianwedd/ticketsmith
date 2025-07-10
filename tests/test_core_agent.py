from ticketsmith.core_agent import CoreAgent


def test_single_loop():
    def llm(_prompt: str) -> str:
        return "Thought: say hello\nAction: echo_tool(message='hi')"

    def echo_tool(message: str) -> str:
        return message

    agent = CoreAgent(llm, {"echo_tool": echo_tool})
    result = agent.run("test")
    history = result.get("history")
    assert history is not None
    assert history[0]["observation"] == "hi"
    assert history[0]["action"]["tool"] == "echo_tool"
    assert history[0]["action"]["args"] == {"message": "hi"}
