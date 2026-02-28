from pydantic import BaseModel, Field
from typing import Any


class IngestTextRequest(BaseModel):
    """payload for ingesting raw text into a collection."""

    collection: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchRequest(BaseModel):
    """payload for a semantic search query."""

    collection: str
    query: str
    limit: int = Field(default=5, ge=1, le=50)


class SearchResult(BaseModel):
    """a single search result with score and payload."""

    id: str | int
    score: float
    payload: dict[str, Any]


class SearchResponse(BaseModel):
    """response wrapper for search results."""

    results: list[SearchResult]
    total: int


class CollectionInfo(BaseModel):
    """info about a single qdrant collection."""

    name: str
    vectors_count: int | None
    points_count: int | None


class CreateCollectionRequest(BaseModel):
    """payload to create a new collection."""

    name: str


class IngestResponse(BaseModel):
    """response after a successful ingest."""

    collection: str
    chunks_ingested: int
    message: str
