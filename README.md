# DevCrew — Multi-Agent AI Orchestration System

An AI software team in a pipeline. You give it a one-line project idea; four specialised LLM agents plan it, code it, test it, and review it — each handing structured output to the next.

Built with **CrewAI** on the OpenAI API.

## How it works

```
 idea ─→ ┌─────────────────┐      ┌─────────────────┐
         │ Project Manager │ ───→ │    Developer    │
         │  plan.json      │      │    code.py      │
         └─────────────────┘      └───────┬─────────┘
                                          │
                                          ▼
         ┌─────────────────┐      ┌─────────────────┐
         │  Code Reviewer  │ ←─── │    QA Tester    │
         │  review.json    │      │ test_report.json│
         └─────────────────┘      └─────────────────┘
          (sees code + QA report)
```

1. **Project Manager** turns the idea into a 3–6 task plan (JSON).
2. **Developer** implements the plan as one runnable Python file.
3. **QA Tester** designs edge-case tests against the code and honestly marks which would fail (JSON).
4. **Code Reviewer** reads the code *and* the QA report, scores it, and gives a verdict (JSON).

## Design decisions

- **Role-scoped context, not one giant prompt.** Each agent only receives what it needs (the developer sees the plan, not the user's raw message). Narrow prompts hallucinate less and stay on task.
- **Structured JSON outputs via Pydantic.** Every non-code output is bound to a schema (`devcrew/schemas.py`), so one agent's output is machine-parseable input for the next — no regex, no parsing failures.
- **Sequential process.** A software pipeline has a natural order; sequential orchestration keeps the run deterministic and debuggable. Every stage is written to `output/` so you can inspect exactly where a run went wrong.
- **Adversarial QA.** The tester is prompted to be sceptical and mark failures honestly, and the reviewer sees the QA report — so the review verdict is grounded in found bugs, not vibes.

## Run it

```bash
git clone https://github.com/agrvasu05/devcrew && cd devcrew
pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY

python main.py "Build a CLI expense tracker with categories and monthly totals"
```

Outputs land in `output/`:

| File | Agent | Contents |
|---|---|---|
| `01_plan.json` | Project Manager | Task breakdown |
| `02_code.py` | Developer | Runnable Python file |
| `03_test_report.json` | QA Tester | Test cases + bugs found |
| `04_review.json` | Code Reviewer | Scores, comments, verdict |

A full example run is committed in [`sample_output/`](sample_output/).

## Stack

Python · CrewAI · OpenAI API · Pydantic

## Project structure

```
devcrew/
├── main.py              # CLI entry point
├── devcrew/
│   ├── agents.py        # 4 agents with role-scoped prompts
│   ├── tasks.py         # pipeline tasks + context hand-offs
│   ├── schemas.py       # Pydantic schemas for structured JSON
│   └── crew.py          # crew assembly (sequential process)
├── sample_output/       # committed example run
├── requirements.txt
└── .env.example
```
