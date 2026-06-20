from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request, status

from app.schemas.telegram import TelegramUpdate
from app.services.rag_service import RagService
from app.services.telegram_service import TelegramService


router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook")
async def handle_telegram_webhook(
    update: TelegramUpdate,
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> dict[str, bool]:
    settings = request.app.state.settings
    if settings.telegram_webhook_secret and (
        x_telegram_bot_api_secret_token != settings.telegram_webhook_secret
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    message = update.message
    if message is None:
        return {"ok": True}

    telegram_service: TelegramService = request.app.state.telegram_service
    if not message.text:
        await telegram_service.send_message(
            message.chat.id,
            "Пока я отвечаю только на текстовые вопросы о Centr Krasok.",
        )
        return {"ok": True}

    rag_service: RagService = request.app.state.rag_service
    await telegram_service.send_typing_action(message.chat.id)
    answer = await rag_service.answer(message.chat.id, message.text)
    await telegram_service.send_message(message.chat.id, answer.text)
    return {"ok": True}

