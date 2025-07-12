from __future__ import annotations

import re
from typing import Any, Callable, Dict

import structlog

from .metrics import ERROR_COUNT, REQUEST_LATENCY

from .memory import ConversationBuffer, SimpleVectorStore
from .tools import ToolDispatcher
from .security import GuardrailModel, sanitize_input, parse_args

from langgraph import graph

logger = structlog.get_logger(__name__)

SYSTEM_PROMPT = (
    "You are a helpful assistant. Only answer with information supported by "
    "the provided context. If the context does not contain the answer, "
    "respond with 'I don't know based on the provided context.'"
)


class CoreAgent:
    """Simple ReAct agent using a LangGraph state machine."""

    def __init__(
        self,
        llm: Callable[[str], str],
        tools: ToolDispatcher,
        conversation_buffer: ConversationBuffer | None = None,
        vector_store: SimpleVectorStore | None = None,
        guardrail: GuardrailModel | None = None,
    ) -> None:
        """Create a CoreAgent.

        Args:
            llm: Function that generates agent output from a prompt.
            tools: Dispatcher used to execute tools by name.
            conversation_buffer: Optional buffer for short-term memory.
            vector_store: Optional long-term memory store.
            guardrail: Optional guardrail model used to classify prompts.
        """
        self.llm = llm
        self.tools = tools
        self.conversation_buffer = conversation_buffer or ConversationBuffer()
        self.vector_store = vector_store
        self.guardrail = guardrail or GuardrailModel()
        self._graph = self._build_graph()

    @staticmethod
    def _build_graph() -> graph.Pregel:
        """Construct the underlying LangGraph state machine."""
        g = graph.Graph()
        g.add_node("thought", CoreAgent._thought_step)
        g.add_node("act", CoreAgent._action_step)
        g.add_node("observe", CoreAgent._observe_step)
        g.add_edge("thought", "act")
        g.add_edge("act", "observe")
        g.set_entry_point("thought")
        g.set_finish_point("observe")
        return g.compile()

    @staticmethod
    def _thought_step(state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the next thought using the LLM."""
        prompt = CoreAgent._build_prompt(state)
        llm = state["llm"]
        state["llm_output"] = llm(prompt)
        logger.info("thought", prompt=prompt, llm_output=state["llm_output"])
        return state

    @staticmethod
    def _action_step(state: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the action and execute the corresponding tool."""
        tool_name, kwargs = CoreAgent.parse_action(state["llm_output"])
        dispatcher: ToolDispatcher = state["tools"]
        state["action"] = {"tool": tool_name, "args": kwargs}
        state["observation"] = dispatcher.dispatch(tool_name, **kwargs)
        logger.info(
            "action",
            tool=tool_name,
            args=kwargs,
            observation=state["observation"],
        )
        return state

    @staticmethod
    def _observe_step(state: Dict[str, Any]) -> Dict[str, Any]:
        """Record the observation in history."""
        history = state.setdefault("history", [])
        history.append(
            {
                "thought": state.get("llm_output"),
                "action": state.get("action"),
                "observation": state.get("observation"),
            }
        )
        logger.info("observe", observation=state.get("observation"))
        return state

    @staticmethod
    def _build_prompt(state: Dict[str, Any]) -> str:
        """Build the prompt for the LLM."""
        prompt = f"{SYSTEM_PROMPT}\n"
        if "context" in state:
            prompt += f"Context: {state['context']}\n"
        for step in state.get("history", []):
            prompt += f"Thought: {step['thought']}\n"
            prompt += f"Action: {step['action']}\n"
            prompt += f"Observation: {step['observation']}\n"
        if "input" in state:
            prompt += f"Input: {state['input']}\n"
        prompt += "Respond with 'Thought: <reasoning>\nAction: <tool>(<args>)'"
        return prompt

    def run(self, text: str) -> Dict[str, Any]:
        """Execute one Thought-Action-Observation loop."""
        sanitized = sanitize_input(text)
        if self.guardrail and not self.guardrail.check(sanitized):
            raise ValueError("Input rejected by guardrail model")
        state: Dict[str, Any] = {
            "input": sanitized,
            "tools": self.tools,
            "llm": self.llm,
        }
        logger.info("run_start", input=sanitized)
        if self.conversation_buffer:
            state["history"] = self.conversation_buffer.get_history()
        if self.vector_store:
            results = self.vector_store.similarity_search(sanitized, top_k=1)
            if results:
                state["context"] = results[0]["text"]
        with REQUEST_LATENCY.time():
            try:
                result = self._graph.invoke(state)
            except Exception:
                ERROR_COUNT.inc()
                raise
        if self.conversation_buffer and result.get("history"):
            self.conversation_buffer.add(result["history"][-1])
        logger.info("run_finish", result=result)
        return result

    @staticmethod
    def parse_action(response: str) -> tuple[str, Dict[str, Any]]:
        """Extract tool name and arguments from LLM output."""
        match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
        if not match:
            raise ValueError("Could not parse action")
        name = match.group(1)
        args_str = match.group(2).strip()
        args = parse_args(args_str)
        return name, args
