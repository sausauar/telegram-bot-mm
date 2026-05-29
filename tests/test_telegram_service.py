from __future__ import annotations

from app.services.telegram_service import MAX_TELEGRAM_MESSAGE_LENGTH, split_message


def test_split_message_keeps_short_text_as_single_part() -> None:
    assert split_message("hello") == ["hello"]


def test_split_message_limits_long_text_parts() -> None:
    text = "a" * (MAX_TELEGRAM_MESSAGE_LENGTH + 100)

    parts = split_message(text)

    assert len(parts) == 2
    assert all(len(part) <= MAX_TELEGRAM_MESSAGE_LENGTH for part in parts)

