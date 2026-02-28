from archivist.server import mcp
from archivist.services import retrieval


@mcp.tool
async def search(query: str, limit: int = 5) -> list[dict]:
    """semantic search over the knowledge base. returns scored document chunks."""
    return await retrieval.search(query, limit)
