from __future__ import annotations

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.telegram_webhook import router as telegram_router
from app.core.config import load_settings
from app.core.logging import configure_logging
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.dialog_memory import DialogMemory
from app.services.guardrails import Guardrails
from app.services.llm_service import LlmService
from app.services.rag_service import RagService
from app.services.retriever import Retriever
from app.services.telegram_service import TelegramService


def create_app() -> FastAPI:
    settings = load_settings()
    configure_logging(settings.log_level)

    repository = KnowledgeRepository(settings.knowledge_base_path)
    documents = repository.load_documents()
    retriever = Retriever(documents)
    guardrails = Guardrails(minimum_score=settings.retrieval_min_score)
    llm_service = LlmService(
        provider=settings.resolved_ai_provider,
        api_key=settings.openai_api_key,
        model=settings.resolved_model,
        base_url=settings.openai_base_url,
        amvera_api_token=settings.amvera_api_token,
        amvera_api_url=settings.amvera_api_url,
    )
    rag_service = RagService(
        retriever=retriever,
        llm_service=llm_service,
        guardrails=guardrails,
        memory=DialogMemory(max_messages=settings.max_history_messages),
        top_k=settings.retrieval_top_k,
    )

    app = FastAPI(title="Centr Krasok Telegram AI Assistant")
    app.state.settings = settings
    app.state.knowledge_document_count = len(documents)
    app.state.telegram_service = TelegramService(settings.telegram_bot_token)
    app.state.rag_service = rag_service
    app.include_router(health_router)
    app.include_router(telegram_router)
    return app


app = create_app()
