from typing import Any

from archivist.config import settings
from archivist.services.strategies.base import Chunk, IngestionStrategy


class SimpleStrategy(IngestionStrategy):
    """naive character-based chunking with overlap. no external parsing deps."""

    async def process_file(self, filename: str, content: bytes, metadata: dict[str, Any]) -> list[Chunk]:
        # TODO: wire in file parsing (pdf, docx, txt)
        raise NotImplementedError("file parsing not yet implemented for simple strategy.")

    async def process_text(self, text: str, metadata: dict[str, Any]) -> list[Chunk]:
        # TODO: implement character-based chunking with overlap
        raise NotImplementedError("text chunking not yet implemented for simple strategy.")
