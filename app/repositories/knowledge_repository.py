from __future__ import annotations

from pathlib import Path

from app.schemas.rag import KnowledgeDocument


class KnowledgeRepository:
    def __init__(self, knowledge_base_path: Path) -> None:
        self._knowledge_base_path = knowledge_base_path

    def load_documents(self) -> list[KnowledgeDocument]:
        if not self._knowledge_base_path.exists():
            return []

        raw_text = self._knowledge_base_path.read_text(encoding="utf-8")
        return self._split_markdown(raw_text)

    @staticmethod
    def _split_markdown(raw_text: str) -> list[KnowledgeDocument]:
        documents: list[KnowledgeDocument] = []
        current_title = "Общая информация"
        current_lines: list[str] = []

        for line in raw_text.splitlines():
            if line.startswith("## "):
                if current_lines:
                    documents.append(
                        _build_document(current_title, "\n".join(current_lines))
                    )
                current_title = line.replace("#", "").strip()
                current_lines = [line]
                continue
            current_lines.append(line)

        if current_lines:
            documents.append(_build_document(current_title, "\n".join(current_lines)))

        return [document for document in documents if document.content.strip()]


def _build_document(title: str, content: str) -> KnowledgeDocument:
    normalized_title = title.strip() or "Общая информация"
    source_id = normalized_title.lower().replace(" ", "-")
    return KnowledgeDocument(
        source_id=source_id,
        title=normalized_title,
        content=content.strip(),
        metadata={"source": "company_knowledge", "title": normalized_title},
    )

