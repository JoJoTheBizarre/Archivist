from typing import Any

from qdrant_client.http.models import FieldCondition, Filter, MatchValue

from archivist.config import settings
from archivist.db.qdrant import get_client
from archivist.services.ingestion import get_embedder


async def search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    embedder = get_embedder()
    query_vector = list(embedder.embed([query]))[0].tolist()

    client = get_client()
    response = await client.query_points(
        collection_name=settings.collection,
        query=query_vector,
        query_filter=Filter(
            must=[FieldCondition(key="type", match=MatchValue(value="document"))]
        ),
        limit=limit,
    )

    return [
        {"id": str(r.id), "score": round(r.score, 4), "payload": r.payload}
        for r in response.points
    ]
