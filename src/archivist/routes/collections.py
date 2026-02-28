from starlette.requests import Request
from starlette.responses import JSONResponse

from archivist.server import mcp
from archivist.db import qdrant as db


@mcp.custom_route("/api/collection", methods=["GET"])
async def get_collection(request: Request) -> JSONResponse:
    info = await db.get_collection_info()
    return JSONResponse(info)
