from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class PlanResult:
    """Result of executing a plan step."""

    step: str
    result: str


class StepPlanner:
    """Simple planner that decomposes tasks into steps and executes them."""

    def __init__(self, llm: Callable[[str], str]) -> None:
        """Create planner with the provided LLM callable."""
        self.llm = llm

    def plan(self, task: str) -> List[str]:
        """Generate a plan for a complex task.

        Args:
            task: High level user request.

        Returns:
            A list of step descriptions.
        """
        prompt = (
            "Break down the following task into a numbered list of steps.\n"
            f"Task: {task}\nSteps:"
        )
        response = self.llm(prompt)
        return self._parse_steps(response)

    def execute(
        self, steps: List[str], executor: Callable[[str], str]
    ) -> List[PlanResult]:
        """Execute each step with the provided executor function."""
        results: List[PlanResult] = []
        for step in steps:
            result = executor(step)
            results.append(PlanResult(step=step, result=result))
        return results

    def reflect(self, task: str, results: List[PlanResult]) -> List[str]:
        """Ask the LLM for a revised plan based on execution results."""
        prompt = f"Task: {task}\n"
        for r in results:
            prompt += f"Step: {r.step}\nResult: {r.result}\n"
        prompt += (
            "The task is not fully solved. "
            "Provide a new plan as a numbered list of steps."
        )
        response = self.llm(prompt)
        return self._parse_steps(response)

    @staticmethod
    def _parse_steps(text: str) -> List[str]:
        """Extract numbered steps from LLM output."""
        steps: List[str] = []
        for line in text.splitlines():
            match = re.match(r"\s*\d+\.\s*(.+)", line)
            if match:
                steps.append(match.group(1).strip())
        if not steps and text.strip():
            steps.append(text.strip())
        return steps
