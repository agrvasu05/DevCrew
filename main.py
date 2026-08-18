"""DevCrew — run an AI software team on a one-line project idea.

Usage:
    python main.py "Build a CLI expense tracker"
"""

import os
import sys

from dotenv import load_dotenv

from devcrew.crew import run


def main() -> None:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Missing OPENAI_API_KEY. Copy .env.example to .env and add your key.")

    if len(sys.argv) < 2:
        sys.exit('Usage: python main.py "your project idea"')

    idea = sys.argv[1]
    os.makedirs("output", exist_ok=True)

    print(f"\n🚀 DevCrew starting on: {idea}\n")
    run(idea)
    print(
        "\n✅ Done. Check the output/ folder:\n"
        "   01_plan.json        — Project Manager's plan\n"
        "   02_code.py          — Developer's code\n"
        "   03_test_report.json — QA Tester's report\n"
        "   04_review.json      — Code Reviewer's verdict\n"
    )


if __name__ == "__main__":
    main()
