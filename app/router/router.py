from __future__ import annotations

from typing import Protocol

from app.router.intents import Intent


class ScoredChunk(Protocol):
    title: str


SMALLTALK_WORDS = {
    "/start",
    "start",
    "привет",
    "здравствуйте",
    "здравствуй",
    "салам",
    "hello",
    "hi",
    "добрый день",
    "доброе утро",
    "добрый вечер",
    "спасибо",
    "благодарю",
}

INTERNAL_PROMPT_MARKERS = (
    "system prompt",
    "ignore previous instructions",
    "ignore all instructions",
    "системный prompt",
    "системный промпт",
    "системные инструкции",
    "внутренние инструкции",
    "внутренние правила",
    "игнорируй все инструкции",
    "игнорируй предыдущие инструкции",
    "покажи prompt",
    "покажи промпт",
    "раскрой prompt",
    "раскрой промпт",
)

PRICE_TERMS = (
    "сколько стоит",
    "стоит",
    "цена",
    "цены",
    "стоимость",
    "прайс",
    "ценник",
)

STOCK_TERMS = (
    "в наличии",
    "наличие",
    "остаток",
    "остатки",
    "есть в продаже",
    "доступен товар",
)

PROMOTION_TERMS = ("акци", "скидк", "спецпредлож")
VACANCY_TERMS = ("ваканс", "зарплат", "работа у вас")
CLIENTS_TERMS = ("клиент", "покупател", "заказчик", "партнер", "партнёр")

COMPANY_OVERVIEW_PATTERNS = (
    "что такое центр красок",
    "что такое centr krasok",
    "чем занимается центр красок",
    "чем занимается компания",
    "расскажи о центре красок",
    "расскажите о центре красок",
    "расскажи про центр красок",
    "расскажите про центр красок",
    "расскажи о вашей компании",
    "расскажите о вашей компании",
    "кто вы",
    "о компании",
    "почему стоит обратиться",
)

PRODUCT_TERMS = (
    "товары",
    "товар",
    "ассортимент",
    "что продаете",
    "что продаёте",
    "что у вас есть",
    "какие материалы",
    "краски",
    "лак",
    "грунтов",
)

BRAND_TERMS = ("бренд", "бренды", "марки", "производители")

SERVICE_TERMS = (
    "услуги",
    "услуга",
    "предоставляете",
    "что вы предлагаете",
    "чем можете помочь",
    "колеровка",
    "подбор цвета",
)

DELIVERY_TERMS = (
    "доставка",
    "доставку",
    "доставляете",
    "самовывоз",
    "забрать из шоурума",
)

UNKNOWN_PRODUCT_EXCLUSIONS = (
    "доставка",
    "самовывоз",
    "услуга",
    "услуги",
    "адрес",
    "контакт",
    "телефон",
    "бренд",
    "бренды",
    "в наличии",
    "наличие",
    "остаток",
)

COMPANY_RELATED_TERMS = (
    "центр красок",
    "centr krasok",
    "компани",
    "магазин",
    "краск",
    "лак",
    "масл",
    "грунтов",
    "пропит",
    "штукатур",
    "колеров",
    "цвет",
    "бренд",
    "товар",
    "продукт",
    "услуг",
    "достав",
    "самовывоз",
    "адрес",
    "контакт",
    "телефон",
    "email",
    "почт",
    "график",
    "режим",
    "дизайнер",
    "строител",
    "клиент",
    "партнер",
    "партнёр",
    "проект",
    "ваканс",
    "зарплат",
    "директор",
    "владел",
    "цена",
    "стоим",
    "налич",
    "акци",
)

OUT_OF_SCOPE_TERMS = (
    "матч",
    "футбол",
    "лига",
    "спорт",
    "прогноз",
    "предскажи",
    "рецепт",
    "плов",
    "погода",
    "курс валют",
    "крипт",
)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).lower().replace("ё", "е")


def detect_intent(text: str) -> Intent:
    normalized = normalize_text(text)
    stripped = normalized.strip("!.,? ")

    if stripped in SMALLTALK_WORDS:
        return Intent.GREETING
    if any(marker in normalized for marker in INTERNAL_PROMPT_MARKERS):
        return Intent.INTERNAL_PROMPT
    if any(pattern in normalized for pattern in COMPANY_OVERVIEW_PATTERNS):
        return Intent.COMPANY_OVERVIEW
    if any(term in normalized for term in PRICE_TERMS):
        return Intent.PRICE
    if any(term in normalized for term in STOCK_TERMS):
        return Intent.STOCK
    if any(term in normalized for term in PROMOTION_TERMS):
        return Intent.PROMOTIONS
    if any(term in normalized for term in VACANCY_TERMS):
        return Intent.VACANCIES
    if any(term in normalized for term in CLIENTS_TERMS):
        return Intent.CLIENTS
    if any(term in normalized for term in DELIVERY_TERMS):
        return Intent.DELIVERY
    if any(term in normalized for term in BRAND_TERMS):
        return Intent.BRANDS
    if any(term in normalized for term in SERVICE_TERMS):
        return Intent.SERVICES
    if any(term in normalized for term in PRODUCT_TERMS):
        return Intent.PRODUCTS
    if is_unknown_product_question(normalized):
        return Intent.UNKNOWN_PRODUCT
    return Intent.GENERAL_RAG


def is_unknown_product_question(text: str) -> bool:
    if not any(marker in text for marker in ("у вас есть", "есть ли")):
        return False
    if any(marker in text for marker in UNKNOWN_PRODUCT_EXCLUSIONS):
        return False
    return bool(
        any(char.isdigit() for char in text)
        or any("a" <= char <= "z" for char in text)
        or "краска " in text
        or "лак " in text
        or "грунтов" in text
    )


def is_out_of_scope_question(text: str, chunks: list[ScoredChunk]) -> bool:
    normalized = normalize_text(text)
    if any(term in normalized for term in COMPANY_RELATED_TERMS):
        return False
    if any(term in normalized for term in OUT_OF_SCOPE_TERMS):
        return True
    return not chunks

