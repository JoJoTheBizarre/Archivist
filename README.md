# archivist

I built this MCP server to give my Claude Code setup a persistent semantic memory — it remembers my coding practices, preferred tools, and conventions across sessions, so Claude gets progressively more familiar with how I work. On top of that, you can embed any PDF into the knowledge base by curling the ingest endpoint, making it easy to ground Claude in documentation or reference material.

## deploy

```bash
cp .env.example .env   # set your config
docker compose up -d
```

## add a pdf

```bash
curl -X POST http://localhost:8000/api/ingest/file -F "file=@/path/to/file.pdf"
```

## connect to claude code

Add this to your `.claude/settings.json` under `mcpServers`:

```json
"archivist": {
  "type": "http",
  "url": "http://localhost:8000/mcp"
}
```
