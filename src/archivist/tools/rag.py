from archivist.server import mcp
from archivist.services import retrieval
from archivist.db import qdrant as db


@mcp.tool
async def search(query: str, limit: int = 5) -> list[dict]:
    """semantic search over the knowledge base. returns scored document chunks."""
    return await retrieval.search(query, limit)


@mcp.tool
async def get_collection_info() -> dict:
    """get info about the active collection: name, point count, status."""
    return await db.get_collection_info()
