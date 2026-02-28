import asyncio
import os
import tempfile
from functools import cached_property
from pathlib import Path
from typing import Any

from archivist.config import settings
from archivist.services.strategies.base import Chunk, IngestionStrategy


class DoclingStrategy(IngestionStrategy):
    @cached_property
    def _converter(self):
        from docling.document_converter import DocumentConverter

        return DocumentConverter()

    @cached_property
    def _chunker(self):
        from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
        from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer

        return HybridChunker(
            tokenizer=HuggingFaceTokenizer.from_pretrained(
                model_name=settings.embedding_model,
                max_tokens=settings.chunk_size,
            ),
            merge_peers=True,
        )

    def _chunks_from_doc(self, doc, metadata: dict[str, Any]) -> list[Chunk]:
        chunks = []
        for chunk in self._chunker.chunk(doc):
            text = self._chunker.contextualize(chunk)
            meta = {
                **metadata,
                "headings": getattr(chunk.meta, "headings", []) or [],
            }
            chunks.append(Chunk(text=text, metadata=meta))
        return chunks

    async def process_file(
        self, filename: str, content: bytes, metadata: dict[str, Any]
    ) -> list[Chunk]:
        suffix = Path(filename).suffix or ".txt"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(content)
            tmp_path = f.name
        try:
            result = await asyncio.to_thread(self._converter.convert, tmp_path)
        finally:
            os.unlink(tmp_path)
        return self._chunks_from_doc(result.document, {**metadata, "source": filename})

    async def process_text(self, text: str, metadata: dict[str, Any]) -> list[Chunk]:
        with tempfile.NamedTemporaryFile(
            suffix=".md", delete=False, mode="w", encoding="utf-8"
        ) as f:
            f.write(text)
            tmp_path = f.name
        try:
            result = await asyncio.to_thread(self._converter.convert, tmp_path)
        finally:
            os.unlink(tmp_path)
        return self._chunks_from_doc(result.document, metadata)
