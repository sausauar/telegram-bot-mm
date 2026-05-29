from __future__ import annotations

from fastapi import APIRouter, Request


router = APIRouter(tags=["health"])


@router.get("/health")
async def health(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    return {
        "status": "ok",
        "environment": settings.app_env,
        "knowledge_documents": request.app.state.knowledge_document_count,
        "telegram_configured": bool(settings.telegram_bot_token),
        "llm_configured": settings.has_llm_provider,
    }

