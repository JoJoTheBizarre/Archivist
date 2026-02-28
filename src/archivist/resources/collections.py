from archivist.server import mcp
from archivist.db import qdrant as db


@mcp.resource("qdrant://collection")
async def collection_resource() -> dict:
    """live info about the active qdrant collection."""
    return await db.get_collection_info()
