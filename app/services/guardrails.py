from __future__ import annotations

from app.schemas.rag import RetrievedChunk


INSUFFICIENT_CONTEXT_ANSWER = (
    "Сейчас у меня недостаточно данных, чтобы точно ответить на этот вопрос. "
    "Я могу помогать по информации о Centr Krasok: товарам, услугам, адресам, "
    "доставке и способам связи. Лучше уточнить детали у менеджера компании."
)


class Guardrails:
    def __init__(self, minimum_score: float) -> None:
        self._minimum_score = minimum_score

    def has_enough_context(self, chunks: list[RetrievedChunk]) -> bool:
        if not chunks:
            return False
        return chunks[0].score >= self._minimum_score

    def insufficient_context_answer(self) -> str:
        return INSUFFICIENT_CONTEXT_ANSWER

