from archivist.server import mcp


SEARCH_GUIDE = """
# archivist search — agent instructions

The search tool queries the document knowledge base using semantic similarity.
It only searches ingested documents — memories are stored separately and never appear here.

---

## tool

### search(query, limit?)
Embed the query and return the closest matching document chunks by cosine similarity.

- query: a natural language question or topic — write it as you would ask it.
- limit: number of results to return (default 5, max 50).

    search(query="what are the procurement thresholds for open tendering?", limit=5)

Each result contains:
- score: similarity score between 0 and 1 — higher is more relevant.
- payload.text: the raw chunk text.
- payload.source: the filename the chunk came from.
- payload.headings: section headings at the point of extraction (docling strategy only).

---

## when to use it

- the user asks a question that could be answered by an ingested document.
- you need to ground your answer in source material rather than general knowledge.
- the user asks "what does the document say about..." or "find information on...".

"""


@mcp.resource("guide://search")
def search_guide() -> str:
    """
    How to use the search tool to query ingested documents.
    Read this before calling search. Covers query style, result shape,
    and when to prefer recall over search.
    """
    return SEARCH_GUIDE
