from __future__ import annotations

import logging
from typing import Any

from app.prompts.assistant_prompt import build_messages
from app.schemas.rag import RetrievedChunk


LOGGER = logging.getLogger(__name__)
INTERNAL_KNOWLEDGE_MARKERS = {
    "Known facts:",
    "Answering rules:",
}


class LlmService:
    def __init__(
        self,
        provider: str,
        api_key: str | None,
        model: str,
        base_url: str | None = None,
        amvera_api_token: str | None = None,
        amvera_api_url: str | None = None,
    ) -> None:
        self._provider = provider
        self._api_key = api_key
        self._model = model
        self._base_url = base_url
        self._amvera_api_token = amvera_api_token
        self._amvera_api_url = amvera_api_url

    async def answer(
        self,
        user_text: str,
        chunks: list[RetrievedChunk],
        history: list[dict[str, str]] | None = None,
    ) -> tuple[str, bool]:
        if self._provider == "openai":
            return await self._answer_with_openai(user_text, chunks, history)
        if self._provider == "amvera":
            return await self._answer_with_amvera(user_text, chunks, history)
        return self._offline_answer(chunks), False

    async def _answer_with_openai(
        self,
        user_text: str,
        chunks: list[RetrievedChunk],
        history: list[dict[str, str]] | None,
    ) -> tuple[str, bool]:
        if not self._api_key:
            return self._offline_answer(chunks), False

        try:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=self._api_key, base_url=self._base_url)
            response = await client.chat.completions.create(
                model=self._model,
                messages=build_messages(user_text, chunks, history),
                temperature=0.2,
                max_tokens=900,
            )
            content = response.choices[0].message.content
            if content:
                return content.strip(), True
        except Exception as exc:  # pragma: no cover - external provider boundary
            LOGGER.warning("OpenAI provider failed, using offline answer: %s", exc)

        return self._offline_answer(chunks), False

    async def _answer_with_amvera(
        self,
        user_text: str,
        chunks: list[RetrievedChunk],
        history: list[dict[str, str]] | None,
    ) -> tuple[str, bool]:
        if not self._amvera_api_token or not self._amvera_api_url:
            return self._offline_answer(chunks), False

        import httpx

        payload = {
            "model": self._model,
            "messages": [
                {"role": message["role"], "text": message["content"]}
                for message in build_messages(user_text, chunks, history)
            ],
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Token": f"Bearer {self._amvera_api_token}",
        }
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(
                    self._amvera_api_url, headers=headers, json=payload
                )
                response.raise_for_status()
            text = _find_text(response.json())
            if text:
                return text.strip(), True
        except Exception as exc:  # pragma: no cover - external provider boundary
            LOGGER.warning("Amvera provider failed, using offline answer: %s", exc)

        return self._offline_answer(chunks), False

    @staticmethod
    def _offline_answer(chunks: list[RetrievedChunk]) -> str:
        facts: list[str] = []
        for chunk in chunks[:2]:
            for raw_line in chunk.content.splitlines():
                line = raw_line.strip(" -#")
                if not line or line == chunk.title or line in INTERNAL_KNOWLEDGE_MARKERS:
                    continue
                if line.startswith("Дата подготовки") or line.startswith("Назначение файла"):
                    continue
                facts.append(line)
                if len(facts) >= 8:
                    break
            if len(facts) >= 8:
                break

        if not facts:
            return (
                "В найденной информации есть близкий контекст, но его недостаточно "
                "для точного ответа. Лучше уточнить вопрос или связаться с менеджером Centr Krasok."
            )

        return "Вот что могу подсказать по информации Centr Krasok:\n" + "\n".join(
            f"- {fact}" for fact in facts
        )


def _find_text(data: Any) -> str | None:
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in ("content", "text", "answer", "response", "message"):
            found = _find_text(data.get(key))
            if found:
                return found
        return _find_text(data.get("choices"))
    if isinstance(data, list):
        for item in data:
            found = _find_text(item)
            if found:
                return found
    return None
