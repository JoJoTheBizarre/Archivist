from starlette.requests import Request
from starlette.responses import JSONResponse

from archivist.server import mcp
from archivist.db.qdrant import get_client


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """liveness check — also pings qdrant to verify connectivity."""
    try:
        client = get_client()
        await client.get_collections()
        qdrant_ok = True
    except Exception:
        qdrant_ok = False

    return JSONResponse({
        "status": "ok" if qdrant_ok else "degraded",
        "service": "archivist",
        "qdrant": "connected" if qdrant_ok else "unreachable",
    })
