from __future__ import annotations

import math
import re
from collections import Counter

from app.schemas.rag import KnowledgeDocument, RetrievedChunk


TOKEN_PATTERN = re.compile(r"[a-zA-Zа-яА-ЯёЁ0-9]+")

STOPWORDS = {
    "а",
    "без",
    "бы",
    "в",
    "вам",
    "вас",
    "где",
    "для",
    "до",
    "и",
    "или",
    "из",
    "как",
    "к",
    "ли",
    "на",
    "не",
    "о",
    "об",
    "от",
    "по",
    "при",
    "про",
    "с",
    "со",
    "у",
    "что",
    "чем",
    "это",
    "я",
}

QUERY_EXPANSIONS = {
    "адрес": ["контакты", "магазин", "салон", "шоурум"],
    "адреса": ["контакты", "магазин", "салон", "шоурум"],
    "где": ["адрес", "контакты", "магазин"],
    "телефон": ["контакты", "связаться"],
    "краски": ["товары", "ассортимент", "бренды"],
    "краска": ["товары", "ассортимент", "бренды"],
    "товар": ["товары", "ассортимент", "бренды"],
    "товары": ["ассортимент", "краски", "бренды"],
    "бренд": ["бренды", "товары"],
    "бренды": ["товары", "ассортимент"],
    "доставка": ["самовывоз", "заказ"],
    "доставки": ["самовывоз", "заказ"],
    "самовывоз": ["доставка", "магазин"],
    "услуги": ["консультация", "подбор", "колеровка"],
    "цена": ["стоимость", "прайс"],
    "цены": ["стоимость", "прайс"],
}


class Retriever:
    def __init__(self, documents: list[KnowledgeDocument]) -> None:
        self._documents = documents
        self._document_tokens = {
            document.source_id: Counter(tokenize(f"{document.title}\n{document.content}"))
            for document in documents
        }
        self._document_frequency = self._build_document_frequency()

    def retrieve(self, query: str, top_k: int) -> list[RetrievedChunk]:
        query_tokens = expand_query(tokenize(query))
        if not query_tokens:
            return []

        query_counts = Counter(query_tokens)
        chunks: list[RetrievedChunk] = []
        for document in self._documents:
            score = self._score(query_counts, document)
            if score <= 0:
                continue
            chunks.append(
                RetrievedChunk(
                    source_id=document.source_id,
                    title=document.title,
                    content=document.content,
                    score=score,
                    metadata=document.metadata,
                )
            )

        chunks.sort(key=lambda chunk: chunk.score, reverse=True)
        return chunks[:top_k]

    def _build_document_frequency(self) -> Counter[str]:
        document_frequency: Counter[str] = Counter()
        for tokens in self._document_tokens.values():
            document_frequency.update(tokens.keys())
        return document_frequency

    def _score(self, query_counts: Counter[str], document: KnowledgeDocument) -> float:
        document_tokens = self._document_tokens[document.source_id]
        document_count = max(len(self._documents), 1)
        title_tokens = set(tokenize(document.title))
        score = 0.0

        for token, query_count in query_counts.items():
            term_frequency = document_tokens.get(token, 0)
            if term_frequency == 0:
                continue
            inverse_document_frequency = (
                math.log((document_count + 1) / (self._document_frequency[token] + 1))
                + 1
            )
            title_boost = 1.6 if token in title_tokens else 1.0
            score += (
                query_count
                * (1 + math.log(term_frequency))
                * inverse_document_frequency
                * title_boost
            )

        return score


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for match in TOKEN_PATTERN.finditer(text.lower().replace("ё", "е")):
        token = match.group(0)
        if len(token) <= 1 or token in STOPWORDS:
            continue
        tokens.append(token)
    return tokens


def expand_query(tokens: list[str]) -> list[str]:
    expanded = list(tokens)
    for token in tokens:
        expanded.extend(QUERY_EXPANSIONS.get(token, []))
    return expanded

