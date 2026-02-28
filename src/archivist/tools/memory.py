import uuid
from datetime import datetime, timezone

from qdrant_client.http.models import (
    Direction,
    FieldCondition,
    Filter,
    MatchValue,
    OrderBy,
    PointStruct,
)

from archivist.db.qdrant import ensure_collection, get_client
from archivist.config import settings
from archivist.server import mcp
from archivist.services.ingestion import get_embedder


@mcp.tool
async def save_memory(content: str, tags: list[str] | None = None) -> dict:
    """embed and persist a memory entry with a timestamp and optional tags."""
    embedder = get_embedder()
    vector = list(embedder.embed([content]))[0].tolist()

    await ensure_collection()
    client = get_client()

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "text": content,
            "type": "memory",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tags": tags or [],
        },
    )

    await client.upsert(collection_name=settings.collection, points=[point])
    return {"saved": True, "id": point.id, "timestamp": point.payload["timestamp"]} #type: ignore


@mcp.tool
async def recall(query: str, limit: int = 5) -> list[dict]:
    """semantic search over saved memories only."""
    embedder = get_embedder()
    vector = list(embedder.embed([query]))[0].tolist()

    client = get_client()
    response = await client.query_points(
        collection_name=settings.collection,
        query=vector,
        query_filter=Filter(
            must=[FieldCondition(key="type", match=MatchValue(value="memory"))]
        ),
        limit=limit,
    )

    return [
        {
            "id": str(r.id),
            "score": round(r.score, 4),
            "content": r.payload.get("text"), #type: ignore
            "timestamp": r.payload.get("timestamp"), #type: ignore
            "tags": r.payload.get("tags", []), #type: ignore
        }
        for r in response.points
    ]


@mcp.tool
async def recent_memories(limit: int = 10) -> list[dict]:
    """list the most recently saved memories in reverse chronological order."""
    client = get_client()
    records, _ = await client.scroll(
        collection_name=settings.collection,
        scroll_filter=Filter(
            must=[FieldCondition(key="type", match=MatchValue(value="memory"))]
        ),
        order_by=OrderBy(key="timestamp", direction=Direction.DESC),
        limit=limit,
        with_payload=True,
    )

    return [
        {
            "id": str(r.id),
            "content": r.payload.get("text"), #type: ignore
            "timestamp": r.payload.get("timestamp"), #type: ignore
            "tags": r.payload.get("tags", []), #type: ignore
        }
        for r in records
    ]
