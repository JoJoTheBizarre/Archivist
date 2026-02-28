from typing import Any

from archivist.services.strategies.base import Chunk, IngestionStrategy


class DoclingStrategy(IngestionStrategy):
    """docling-powered parsing with hybrid chunking. structure-aware, RAG-optimised."""

    async def process_file(self, filename: str, content: bytes, metadata: dict[str, Any]) -> list[Chunk]:
        # TODO: use DocumentConverter + HybridChunker
        raise NotImplementedError("docling strategy not yet implemented.")

    async def process_text(self, text: str, metadata: dict[str, Any]) -> list[Chunk]:
        # TODO: wrap text in a docling document and apply HybridChunker
        raise NotImplementedError("docling text strategy not yet implemented.")
