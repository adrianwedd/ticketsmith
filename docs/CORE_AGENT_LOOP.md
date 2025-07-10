# Core Agent Loop

The agent follows a simple ReAct loop implemented with LangGraph:

1. **Thought** – the LLM reasons about the current state and decides on an action.
2. **Action** – the chosen tool is invoked with parsed arguments.
3. **Observation** – the tool output is recorded and fed back into the next prompt.

The `CoreAgent` class in `src/ticketsmith/core_agent.py` runs one iteration of this loop and maintains a history of steps.
