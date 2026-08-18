"""Assemble the crew and run the pipeline end-to-end."""

from crewai import Crew, Process

from . import agents, tasks


def build_crew() -> Crew:
    llm = agents.get_llm()

    pm = agents.project_manager(llm)
    dev = agents.developer(llm)
    qa = agents.qa_tester(llm)
    reviewer = agents.code_reviewer(llm)

    t_plan = tasks.plan_task(pm)
    t_code = tasks.code_task(dev, plan=t_plan)
    t_test = tasks.test_task(qa, code=t_code)
    t_review = tasks.review_task(reviewer, code=t_code, tests=t_test)

    return Crew(
        agents=[pm, dev, qa, reviewer],
        tasks=[t_plan, t_code, t_test, t_review],
        process=Process.sequential,  # strict order: plan -> code -> test -> review
        verbose=True,
    )


def run(idea: str) -> str:
    """Run the full pipeline for a one-line project idea."""
    crew = build_crew()
    result = crew.kickoff(inputs={"idea": idea})
    return str(result)
