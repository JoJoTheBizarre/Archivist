from archivist.server import mcp
from archivist.db import qdrant as db


@mcp.resource("qdrant://collections")
async def collections_resource() -> list[dict]:
    """live list of all qdrant collections — read-only context for agents."""
    return await db.list_collections()
