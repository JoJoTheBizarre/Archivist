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
        "Archivist is a RAG knowledge base server. "
        "Use the search tool to retrieve relevant document chunks from a collection. "
        "Use get_collection_info to inspect the knowledge base."
    ),
    lifespan=lifespan,
)
