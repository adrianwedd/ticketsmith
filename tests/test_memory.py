from ticketsmith.core_agent import CoreAgent
from ticketsmith.memory import ConversationBuffer, SimpleVectorStore
from ticketsmith.tools import ToolDispatcher, tool


def test_conversation_buffer_window():
    buffer = ConversationBuffer(window_size=2)

    def llm(_prompt: str) -> str:
        return "Thought: hi\nAction: echo_tool(message='x')"

    @tool(name="echo_tool", description="Return the message.")
    def echo_tool(message: str) -> str:
        return message

    dispatcher = ToolDispatcher([echo_tool])
    agent = CoreAgent(llm, dispatcher, conversation_buffer=buffer)
    agent.run("one")
    assert len(buffer.get_history()) == 1
    agent.run("two")
    assert len(buffer.get_history()) == 2
    agent.run("three")
    assert len(buffer.get_history()) == 2


def test_vector_store_retrieval(tmp_path):
    store_path = tmp_path / "store.json"
    store = SimpleVectorStore(str(store_path))
    store.add("hello world")
    store.add("goodbye")
    results = store.similarity_search("hello", top_k=1)
    assert results[0]["text"] == "hello world"
