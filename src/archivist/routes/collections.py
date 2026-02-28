import json

from starlette.requests import Request
from starlette.responses import JSONResponse

from archivist.server import mcp
from archivist.db import qdrant as db


@mcp.custom_route("/api/collections", methods=["GET"])
async def get_collections(request: Request) -> JSONResponse:
    """list all qdrant collections."""
    collections = await db.list_collections()
    return JSONResponse(collections)


@mcp.custom_route("/api/collections", methods=["POST"])
async def create_collection(request: Request) -> JSONResponse:
    """create a new qdrant collection."""
    body = await request.json()
    name = body.get("name", "").strip()
    if not name:
        return JSONResponse({"error": "collection name is required."}, status_code=400)

    await db.ensure_collection(name)
    return JSONResponse({"collection": name, "message": "collection created."}, status_code=201)


@mcp.custom_route("/api/collections/{name}", methods=["DELETE"])
async def delete_collection(request: Request) -> JSONResponse:
    """delete a qdrant collection by name."""
    name = request.path_params["name"]
    deleted = await db.delete_collection(name)
    if not deleted:
        return JSONResponse({"error": f"collection '{name}' not found."}, status_code=404)
    return JSONResponse({"collection": name, "message": "collection deleted."})
