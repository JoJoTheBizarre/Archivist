from fastmcp import FastMCP

mcp = FastMCP(
    name="archivist",
    instructions=(
        "Archivist is a RAG knowledge base server. "
        "Use the search tool to retrieve relevant document chunks from a collection. "
        "Use list_collections to discover available knowledge bases. "
        "Use get_collection_info to inspect a specific collection."
    ),
)
