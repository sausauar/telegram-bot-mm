from __future__ import annotations

from pydantic import BaseModel, Field


class TelegramChat(BaseModel):
    id: int


class TelegramUser(BaseModel):
    id: int | None = None
    first_name: str | None = None
    username: str | None = None


class TelegramMessage(BaseModel):
    message_id: int
    chat: TelegramChat
    text: str | None = None
    from_user: TelegramUser | None = Field(default=None, alias="from")


class TelegramUpdate(BaseModel):
    update_id: int
    message: TelegramMessage | None = None

