from functools import lru_cache
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams
from archivist.config import settings


@lru_cache(maxsize=1)
def get_client() -> AsyncQdrantClient:
    return AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key,
    )


async def ensure_collection() -> None:
    client = get_client()
    if not await client.collection_exists(settings.collection):
        await client.create_collection(
            collection_name=settings.collection,
            vectors_config=VectorParams(
                size=settings.embedding_dim,
                distance=Distance.COSINE,
            ),
        )


async def get_collection_info() -> dict:
    client = get_client()
    info = await client.get_collection(settings.collection)
    return {
        "name": settings.collection,
        "points_count": info.points_count,
        "status": str(info.status),
    }
