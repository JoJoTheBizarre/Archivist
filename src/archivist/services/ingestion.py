from typing import Any

# TODO: implement full parsing → chunking → embedding → upsert pipeline.
# this is a stub — the ingestion logic will be fleshed out separately.


async def ingest_text(
    collection: str, text: str, metadata: dict[str, Any] | None = None
) -> int:
    """stub: ingest raw text into a collection. returns number of chunks ingested."""
    raise NotImplementedError("ingestion pipeline not yet implemented.")


async def ingest_file(
    collection: str, filename: str, content: bytes, metadata: dict[str, Any] | None = None
) -> int:
    """stub: parse a file and ingest its text. returns number of chunks ingested."""
    raise NotImplementedError("file ingestion pipeline not yet implemented.")
