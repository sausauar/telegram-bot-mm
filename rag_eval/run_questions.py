from __future__ import annotations

import asyncio
import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

parser = argparse.ArgumentParser(description="Run RAG evaluation questions.")
parser.add_argument(
    "--offline",
    action="store_true",
    help="Use offline fallback instead of the configured LLM provider.",
)
parser.add_argument(
    "--delay",
    type=float,
    default=0.0,
    help="Sleep between questions to avoid provider rate limits.",
)
parser.add_argument(
    "--range",
    type=str,
    default=None,
    help="Filter questions by number range, e.g. 23-43.",
)
args = parser.parse_args()
if args.offline:
    os.environ["AI_PROVIDER"] = "offline"

from app.main import app


QUESTION_PATTERN = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")
QUESTIONS_PATH = PROJECT_ROOT / "rag_eval" / "questions.md"
ANSWERS_DIR = PROJECT_ROOT / "rag_eval" / "answers"


def load_questions() -> list[tuple[int, str]]:
    questions: list[tuple[int, str]] = []
    for line in QUESTIONS_PATH.read_text(encoding="utf-8").splitlines():
        match = QUESTION_PATTERN.match(line)
        if match:
            questions.append((int(match.group(1)), match.group(2)))
    return questions


def filter_questions(
    questions: list[tuple[int, str]], range_str: str | None
) -> list[tuple[int, str]]:
    if range_str is None:
        return questions
    start, end = map(int, range_str.split("-"))
    return [(n, q) for n, q in questions if start <= n <= end]


async def main() -> None:
    ANSWERS_DIR.mkdir(parents=True, exist_ok=True)
    questions = filter_questions(load_questions(), args.range)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = ANSWERS_DIR / f"rag_run_{timestamp}.md"

    lines = [
        f"# RAG Run {timestamp}",
        "",
        f"Questions: {len(questions)}",
        "",
    ]

    for number, question in questions:
        chat_id = 20_000 if number >= 40 else 10_000 + number
        answer = await app.state.rag_service.answer(chat_id, question)
        source_titles = [source.title for source in answer.sources]
        lines.extend(
            [
                f"## {number}. {question}",
                "",
                f"used_llm: `{answer.used_llm}`",
                f"sources: `{source_titles}`",
                "",
                answer.text,
                "",
            ]
        )
        if args.delay > 0:
            await asyncio.sleep(args.delay)

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    asyncio.run(main())