from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import JSONResponse

from archivist.server import mcp
from archivist.config import settings
from archivist.services import ingestion


@mcp.custom_route("/api/ingest/file", methods=["POST"])
async def ingest_file(request: Request) -> JSONResponse:
    form = await request.form()
    file = form.get("file")

    if not isinstance(file, UploadFile) or not file.filename:
        return JSONResponse({"error": "file is required."}, status_code=400)

    content = await file.read()
    _ = await ingestion.ingest_file(file.filename, content)
    return JSONResponse(
        {
            "collection": settings.collection,
            "source": file.filename,
        }
    )


@mcp.custom_route("/api/ingest/text", methods=["POST"])
async def ingest_text(request: Request) -> JSONResponse:
    body = await request.json()
    text = body.get("text", "").strip()
    metadata = body.get("metadata", {})

    if not text:
        return JSONResponse({"error": "text is required."}, status_code=400)

    chunks = await ingestion.ingest_text(text, metadata)
    return JSONResponse(
        {
            "collection": settings.collection,
            "chunks_ingested": chunks,
        }
    )


@mcp.custom_route("/api/documents/{doc_id}", methods=["DELETE"])
async def delete_document(request: Request) -> JSONResponse:
    doc_id = request.path_params["doc_id"]

    from archivist.db.qdrant import get_client
    from qdrant_client.models import PointIdsList

    client = get_client()
    await client.delete(
        collection_name=settings.collection,
        points_selector=PointIdsList(points=[doc_id]),
    )
    return JSONResponse(
        {"id": doc_id, "collection": settings.collection, "deleted": True}
    )
