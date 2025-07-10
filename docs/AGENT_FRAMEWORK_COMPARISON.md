# Agent Framework Comparison

The following table summarizes the evaluation of agent frameworks for TicketSmith.

| Framework  | Approach | Strengths | Weaknesses |
|-----------|----------|-----------|------------|
| **LangGraph** | Explicit state management via DAG of nodes | Predictable, auditable workflows; easier debugging | More upfront design effort |
| **AutoGen** | Emergent agent-to-agent conversation | Flexible and dynamic; less setup | Harder to predict; challenging to debug |

**Decision:** For production workflows requiring reliability and auditability, LangGraph is preferred. AutoGen may be explored for experimental features where flexibility outweighs strict control.
