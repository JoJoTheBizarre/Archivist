from functools import lru_cache
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams
from archivist.config import settings


@lru_cache(maxsize=1)
def get_client() -> AsyncQdrantClient:
    """return a cached async qdrant client."""
    return AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key,
    )


async def ensure_collection(collection: str) -> None:
    """create the collection if it doesn't already exist."""
    client = get_client()
    exists = await client.collection_exists(collection)
    if not exists:
        await client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(
                size=settings.embedding_dim,
                distance=Distance.COSINE,
            ),
        )


async def list_collections() -> list[dict]:
    """return a list of collection info dicts."""
    client = get_client()
    response = await client.get_collections()
    result = []
    for col in response.collections:
        info = await client.get_collection(col.name)
        result.append(
            {
                "name": col.name,
                "points_count": info.points_count,
            }
        )
    return result


async def delete_collection(collection: str) -> bool:
    """delete a collection, returns True if it existed."""
    client = get_client()
    exists = await client.collection_exists(collection)
    if not exists:
        return False
    await client.delete_collection(collection)
    return True
