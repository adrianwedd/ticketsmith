from ticketsmith.planning import StepPlanner, PlanResult


def test_plan_and_execute():
    def llm(prompt: str) -> str:
        return "1. first\n2. second"

    planner = StepPlanner(llm)
    steps = planner.plan("do stuff")
    assert steps == ["first", "second"]

    def executor(step: str) -> str:
        return f"{step} done"

    results = planner.execute(steps, executor)
    assert results[0].result == "first done"
    assert results[1].result == "second done"


def test_reflect():
    responses = {
        "plan": "1. step",
        "reflect": "1. new step",
    }

    def llm(prompt: str) -> str:
        if "The task is not fully solved" in prompt:
            return responses["reflect"]
        return responses["plan"]

    planner = StepPlanner(llm)
    steps = planner.plan("task")
    results = [PlanResult(step=steps[0], result="failure")]
    new_steps = planner.reflect("task", results)
    assert new_steps == ["new step"]
