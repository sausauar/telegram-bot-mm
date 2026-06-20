from __future__ import annotations

import logging

import httpx


LOGGER = logging.getLogger(__name__)
MAX_TELEGRAM_MESSAGE_LENGTH = 3900


class TelegramService:
    def __init__(self, bot_token: str | None) -> None:
        self._bot_token = bot_token

    async def send_typing_action(self, chat_id: int) -> None:
        await self._call("sendChatAction", {"chat_id": chat_id, "action": "typing"})

    async def send_message(self, chat_id: int, text: str) -> None:
        for part in split_message(text):
            await self._call(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": part,
                    "disable_web_page_preview": True,
                },
            )

    async def _call(self, method: str, payload: dict[str, object]) -> None:
        if not self._bot_token:
            LOGGER.info("Telegram token is not configured. Skipping %s.", method)
            return

        url = f"https://api.telegram.org/bot{self._bot_token}/{method}"
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()


def split_message(text: str) -> list[str]:
    if len(text) <= MAX_TELEGRAM_MESSAGE_LENGTH:
        return [text]

    parts: list[str] = []
    remaining = text
    while len(remaining) > MAX_TELEGRAM_MESSAGE_LENGTH:
        split_at = remaining.rfind("\n", 0, MAX_TELEGRAM_MESSAGE_LENGTH)
        if split_at == -1:
            split_at = MAX_TELEGRAM_MESSAGE_LENGTH
        parts.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()

    if remaining:
        parts.append(remaining)
    return parts

