from __future__ import annotations

from app.schemas.rag import KnowledgeDocument
from app.services.retriever import Retriever


def test_retriever_returns_relevant_company_chunk() -> None:
    documents = [
        KnowledgeDocument(
            source_id="products",
            title="Товары",
            content="Компания продает краски, грунтовки, лаки и малярные инструменты.",
            metadata={"source": "test"},
        ),
        KnowledgeDocument(
            source_id="contacts",
            title="Контакты",
            content="Адрес и телефон нужно уточнять у менеджера.",
            metadata={"source": "test"},
        ),
    ]

    chunks = Retriever(documents).retrieve("Какие краски продает компания?", top_k=1)

    assert chunks
    assert chunks[0].source_id == "products"

