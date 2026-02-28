from archivist.server import mcp
from archivist.db import qdrant as db
from archivist.services import retrieval


@mcp.tool
async def search(collection: str, query: str, limit: int = 5) -> list[dict]:
    """semantic search over a qdrant collection. returns scored document chunks."""
    return await retrieval.search(collection, query, limit)


@mcp.tool
async def list_collections() -> list[dict]:
    """list all available qdrant collections with their point counts."""
    return await db.list_collections()


@mcp.tool
async def get_collection_info(collection: str) -> dict:
    """get detailed info about a specific qdrant collection."""
    from archivist.db.qdrant import get_client
    client = db.get_client()
    info = await client.get_collection(collection)
    return {
        "name": collection,
        "vectors_count": info.vectors_count,
        "points_count": info.points_count,
        "status": str(info.status),
    }
