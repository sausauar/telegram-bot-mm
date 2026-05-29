from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeDocument:
    source_id: str
    title: str
    content: str
    metadata: dict[str, str]


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    source_id: str
    title: str
    content: str
    score: float
    metadata: dict[str, str]


@dataclass(frozen=True, slots=True)
class RagAnswer:
    text: str
    sources: list[RetrievedChunk]
    used_llm: bool

