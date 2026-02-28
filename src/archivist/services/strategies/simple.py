import io
from typing import Any

from archivist.config import settings
from archivist.services.strategies.base import Chunk, IngestionStrategy


def _parse(filename: str, content: bytes) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        from docx import Document

        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    return content.decode("utf-8", errors="replace")


def _chunk(text: str) -> list[str]:
    size, overlap = settings.chunk_size, settings.chunk_overlap
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size - overlap
    return [c for c in chunks if c.strip()]


class SimpleStrategy(IngestionStrategy):
    async def process_file(
        self, filename: str, content: bytes, metadata: dict[str, Any]
    ) -> list[Chunk]:
        text = _parse(filename, content)
        return [
            Chunk(text=c, metadata={**metadata, "source": filename})
            for c in _chunk(text)
        ]

    async def process_text(self, text: str, metadata: dict[str, Any]) -> list[Chunk]:
        return [Chunk(text=c, metadata=metadata) for c in _chunk(text)]
