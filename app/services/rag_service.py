from __future__ import annotations

from app.policies.answer_policy import OUT_OF_SCOPE_ANSWER, build_deterministic_answer
from app.policies.voice import apply_company_voice
from app.router.router import detect_intent, is_out_of_scope_question, is_repeat_request
from app.schemas.rag import RagAnswer
from app.services.dialog_memory import DialogMemory
from app.services.guardrails import Guardrails
from app.services.llm_service import LlmService
from app.services.retriever import Retriever


class RagService:
    def __init__(
        self,
        retriever: Retriever,
        llm_service: LlmService,
        guardrails: Guardrails,
        memory: DialogMemory,
        top_k: int,
    ) -> None:
        self._retriever = retriever
        self._llm_service = llm_service
        self._guardrails = guardrails
        self._memory = memory
        self._top_k = top_k

    async def answer(self, chat_id: int, user_text: str) -> RagAnswer:
        cleaned_text = " ".join(user_text.split())
        if not cleaned_text:
            return RagAnswer(
                text="Напишите вопрос о Centr Krasok, и я помогу по информации компании.",
                sources=[],
                used_llm=False,
            )

        if is_repeat_request(cleaned_text):
            repeated_answer = self._short_repeat(chat_id)
            if repeated_answer:
                self._remember(chat_id, cleaned_text, repeated_answer)
                return RagAnswer(text=repeated_answer, sources=[], used_llm=False)

        intent = detect_intent(cleaned_text)
        deterministic_answer = build_deterministic_answer(intent)
        if deterministic_answer:
            self._remember(chat_id, cleaned_text, deterministic_answer)
            return RagAnswer(text=deterministic_answer, sources=[], used_llm=False)

        chunks = self._retriever.retrieve(cleaned_text, top_k=self._top_k)
        if is_out_of_scope_question(cleaned_text, chunks):
            self._remember(chat_id, cleaned_text, OUT_OF_SCOPE_ANSWER)
            return RagAnswer(text=OUT_OF_SCOPE_ANSWER, sources=[], used_llm=False)

        if not self._guardrails.has_enough_context(chunks):
            answer_text = self._guardrails.insufficient_context_answer()
            self._remember(chat_id, cleaned_text, answer_text)
            return RagAnswer(text=answer_text, sources=chunks, used_llm=False)

        answer_text, used_llm = await self._llm_service.answer(
            cleaned_text, chunks, self._memory.get(chat_id)
        )
        answer_text = apply_company_voice(answer_text)
        self._remember(chat_id, cleaned_text, answer_text)
        return RagAnswer(text=answer_text, sources=chunks, used_llm=used_llm)

    def _remember(self, chat_id: int, user_text: str, answer_text: str) -> None:
        self._memory.add(chat_id, "user", user_text)
        self._memory.add(chat_id, "assistant", answer_text)

    def _short_repeat(self, chat_id: int) -> str | None:
        for message in reversed(self._memory.get(chat_id)):
            if message["role"] != "assistant":
                continue
            text = " ".join(message["content"].split())
            if not text:
                continue
            if len(text) <= 260:
                return text
            return text[:257].rstrip(" ,.;:") + "..."
        return None
