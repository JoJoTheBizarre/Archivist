from contextlib import asynccontextmanager
from fastmcp import FastMCP


@asynccontextmanager
async def lifespan(server: FastMCP):
    from archivist.db.qdrant import ensure_collection

    await ensure_collection()
    yield


mcp = FastMCP(
    name="archivist",
    instructions=(
        "Archivist is a RAG knowledge base server with semantic memory. "
        "Read guide://server for a full overview of what this server provides. "
        "Read guide://search to understand how to query ingested documents. "
        "Read guide://memory to understand how to save and recall agent memories."
    ),
    lifespan=lifespan,
)
