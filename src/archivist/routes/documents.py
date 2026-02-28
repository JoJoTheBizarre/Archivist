from starlette.requests import Request
from starlette.responses import JSONResponse

from archivist.server import mcp
from archivist.services import ingestion


@mcp.custom_route("/api/ingest/file", methods=["POST"])
async def ingest_file(request: Request) -> JSONResponse:
    """upload a file (pdf, docx, txt) and ingest it into a collection."""
    form = await request.form()
    collection = form.get("collection", "").strip()
    file = form.get("file")

    if not collection:
        return JSONResponse({"error": "collection is required."}, status_code=400)
    if file is None:
        return JSONResponse({"error": "file is required."}, status_code=400)

    content = await file.read()
    chunks = await ingestion.ingest_file(collection, file.filename, content)
    return JSONResponse(
        {
            "collection": collection,
            "chunks_ingested": chunks,
            "message": f"ingested {chunks} chunks from '{file.filename}'.",
        }
    )


@mcp.custom_route("/api/ingest/text", methods=["POST"])
async def ingest_text(request: Request) -> JSONResponse:
    """ingest raw text directly into a collection."""
    body = await request.json()
    collection = body.get("collection", "").strip()
    text = body.get("text", "").strip()
    metadata = body.get("metadata", {})

    if not collection:
        return JSONResponse({"error": "collection is required."}, status_code=400)
    if not text:
        return JSONResponse({"error": "text is required."}, status_code=400)

    chunks = await ingestion.ingest_text(collection, text, metadata)
    return JSONResponse(
        {
            "collection": collection,
            "chunks_ingested": chunks,
            "message": f"ingested {chunks} chunks.",
        }
    )


@mcp.custom_route("/api/documents/{collection}/{doc_id}", methods=["DELETE"])
async def delete_document(request: Request) -> JSONResponse:
    """delete a document point by collection and id."""
    collection = request.path_params["collection"]
    doc_id = request.path_params["doc_id"]

    from archivist.db.qdrant import get_client
    from qdrant_client.models import PointIdsList

    client = get_client()
    await client.delete(
        collection_name=collection,
        points_selector=PointIdsList(points=[doc_id]),
    )
    return JSONResponse(
        {
            "collection": collection,
            "id": doc_id,
            "message": "document deleted.",
        }
    )
