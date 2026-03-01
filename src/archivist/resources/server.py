from archivist.server import mcp


SERVER_OVERVIEW = """
# archivist — server overview

Archivist is a RAG knowledge base server with semantic memory.
It stores two distinct types of data in the same Qdrant vector collection,
isolated by a type tag so they never mix in search results.

---

## what it stores

### documents  (type: document)
Ingested files and text chunks — PDFs, DOCX, plain text — split into chunks,
embedded, and indexed for semantic retrieval. Searched with the search tool.

### memories  (type: memory)
Agent diary entries — user preferences, decisions, conventions, and facts
observed across sessions. Searched with recall, listed with recent_memories.


## tools available

| tool              | searches    | description                                      |
|-------------------|-------------|--------------------------------------------------|
| search            | documents   | semantic search over ingested document chunks that may exist   |
| save_memory       | —           | persist a memory entry with timestamp and tags   |
| recall            | memories    | semantic search over saved memories              |

---

## resources available

| uri               | description                                              |
|-------------------|----------------------------------------------------------|
| guide://server      | this overview                                            |
| guide://search      | how to use the search tool and what it retrieves         |
| guide://memory      | how to use the memory tools and post-task save habit     |


## recommended session start

1. read guide://memory — prime yourself on the memory system.
2. call recent_memories(limit=5) — catch up on recent context about the user.
4. after the task, call save_memory with a one-sentence preference summary.
"""


@mcp.resource("guide://server")
def server_overview() -> str:
    """
    Full overview of the archivist server: what it stores, which tools exist,
    which resources are available, and the recommended session start sequence.
    Read this first.
    """
    return SERVER_OVERVIEW
