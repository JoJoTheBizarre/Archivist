import uuid
from functools import lru_cache
from typing import Any

from fastembed import TextEmbedding
from qdrant_client.models import PointStruct

from archivist.config import settings
from archivist.db.qdrant import ensure_collection, get_client
from archivist.services.strategies.base import Chunk, IngestionStrategy


@lru_cache(maxsize=1)
def get_embedder() -> TextEmbedding:
    return TextEmbedding(model_name=settings.embedding_model)


@lru_cache(maxsize=1)
def get_strategy() -> IngestionStrategy:
    if settings.ingestion_strategy == "docling":
        from archivist.services.strategies.docling import DoclingStrategy

        return DoclingStrategy()
    from archivist.services.strategies.simple import SimpleStrategy

    return SimpleStrategy()


async def _embed_and_upsert(chunks: list[Chunk]) -> int:
    if not chunks:
        return 0

    embedder = get_embedder()
    embeddings = list(embedder.embed([c.text for c in chunks]))

    await ensure_collection()
    client = get_client()

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=emb.tolist(),
            payload={"text": c.text, "type": "document", **c.metadata},
        )
        for c, emb in zip(chunks, embeddings)
    ]

    await client.upsert(collection_name=settings.collection, points=points)
    return len(points)


async def ingest_file(
    filename: str, content: bytes, metadata: dict[str, Any] | None = None
) -> int:
    chunks = await get_strategy().process_file(filename, content, metadata or {})
    return await _embed_and_upsert(chunks)


async def ingest_text(text: str, metadata: dict[str, Any] | None = None) -> int:
    chunks = await get_strategy().process_text(text, metadata or {})
    return await _embed_and_upsert(chunks)
