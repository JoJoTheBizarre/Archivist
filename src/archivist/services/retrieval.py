from typing import Any

from archivist.config import settings
from archivist.db.qdrant import get_client
from archivist.services.ingestion import get_embedder


async def search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    embedder = get_embedder()
    query_vector = list(embedder.embed([query]))[0].tolist()

    client = get_client()
    results = await client.search(
        collection_name=settings.collection,
        query_vector=query_vector,
        limit=limit,
    )

    return [
        {"id": str(r.id), "score": round(r.score, 4), "payload": r.payload}
        for r in results
    ]
