from __future__ import annotations

import re
from typing import Any, Callable, Dict

from langgraph import graph


class CoreAgent:
    """Simple ReAct agent using a LangGraph state machine."""

    def __init__(
        self, llm: Callable[[str], str], tools: Dict[str, Callable[..., Any]]
    ) -> None:
        """Create a CoreAgent.

        Args:
            llm: Function that generates a thought and action text from a
                prompt.
            tools: Mapping of tool names to callables.
        """
        self.llm = llm
        self.tools = tools
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
        return state

    @staticmethod
    def _action_step(state: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the action and execute the corresponding tool."""
        tool_name, kwargs = CoreAgent.parse_action(state["llm_output"])
        tool = state["tools"].get(tool_name)
        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")
        state["action"] = {"tool": tool_name, "args": kwargs}
        state["observation"] = tool(**kwargs)
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
        return state

    @staticmethod
    def _build_prompt(state: Dict[str, Any]) -> str:
        """Build the prompt for the LLM."""
        prompt = ""
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
        state: Dict[str, Any] = {
            "input": text,
            "tools": self.tools,
            "llm": self.llm,
        }
        return self._graph.invoke(state)

    @staticmethod
    def parse_action(response: str) -> tuple[str, Dict[str, Any]]:
        """Extract tool name and arguments from LLM output."""
        match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
        if not match:
            raise ValueError("Could not parse action")
        name = match.group(1)
        args_str = match.group(2).strip()
        args = {}
        if args_str:
            args = eval(f"dict({args_str})", {"__builtins__": {"dict": dict}})
        return name, args
