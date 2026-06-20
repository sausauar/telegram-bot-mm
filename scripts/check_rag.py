from __future__ import annotations

import asyncio
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import load_settings
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.dialog_memory import DialogMemory
from app.services.guardrails import Guardrails
from app.services.llm_service import LlmService
from app.services.rag_service import RagService
from app.services.retriever import Retriever


async def main() -> None:
    settings = load_settings()
    documents = KnowledgeRepository(settings.knowledge_base_path).load_documents()
    rag_service = RagService(
        retriever=Retriever(documents),
        llm_service=LlmService(provider="offline", api_key=None, model=settings.openai_model),
        guardrails=Guardrails(settings.retrieval_min_score),
        memory=DialogMemory(max_messages=settings.max_history_messages),
        top_k=settings.retrieval_top_k,
    )
    answer = await rag_service.answer(1, "Какие товары есть в Centr Krasok?")
    print(f"documents={len(documents)} sources={len(answer.sources)} used_llm={answer.used_llm}")
    print(answer.text)


if __name__ == "__main__":
    asyncio.run(main())
