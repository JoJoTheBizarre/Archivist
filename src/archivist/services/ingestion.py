from functools import lru_cache
from typing import Any

from archivist.config import settings
from archivist.services.strategies.base import IngestionStrategy


@lru_cache(maxsize=1)
def get_strategy() -> IngestionStrategy:
    if settings.ingestion_strategy == "docling":
        from archivist.services.strategies.docling import DoclingStrategy
        return DoclingStrategy()
    from archivist.services.strategies.simple import SimpleStrategy
    return SimpleStrategy()


async def ingest_file(collection: str, filename: str, content: bytes, metadata: dict[str, Any] | None = None) -> int:
    from archivist.db.qdrant import ensure_collection, get_client
    from qdrant_client.models import PointStruct
    import uuid

    strategy = get_strategy()
    chunks = await strategy.process_file(filename, content, metadata or {})

    await ensure_collection(collection)
    client = get_client()

    points = [
        PointStruct(id=str(uuid.uuid4()), vector=[], payload={"text": c.text, **c.metadata})
        for c in chunks
    ]
    await client.upsert(collection_name=collection, points=points)
    return len(points)


async def ingest_text(collection: str, text: str, metadata: dict[str, Any] | None = None) -> int:
    from archivist.db.qdrant import ensure_collection, get_client
    from qdrant_client.models import PointStruct
    import uuid

    strategy = get_strategy()
    chunks = await strategy.process_text(text, metadata or {})

    await ensure_collection(collection)
    client = get_client()

    points = [
        PointStruct(id=str(uuid.uuid4()), vector=[], payload={"text": c.text, **c.metadata})
        for c in chunks
    ]
    await client.upsert(collection_name=collection, points=points)
    return len(points)
