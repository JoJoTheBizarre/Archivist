from typing import Any

# TODO: implement semantic search with fastembed + qdrant query pipeline.
# this is a stub — retrieval logic will be fleshed out separately.


async def search(collection: str, query: str, limit: int = 5) -> list[dict[str, Any]]:
    """stub: semantic search over a collection. returns scored results."""
    raise NotImplementedError("retrieval pipeline not yet implemented.")
