from archivist.server import mcp


MEMORY_GUIDE = """
# archivist memory — agent instructions

You have access to a semantic memory system backed by a vector database.
Treat it as a personal diary: save meaningful things, recall them when relevant.

---

## tools

### save_memory(content, tags?)
Persist a memory entry. Call this when:
- the user shares something personal, a preference, a goal, or a decision
- something important happens that should be remembered across sessions
- the user explicitly asks you to remember something
- you learn a fact about the user that would be useful later

tags are optional lowercase labels (e.g. ["preference", "tools", "project"]).
Write content in plain, retrievable language — as if writing a diary entry.

    save_memory(
        content="the user prefers dark mode and uses neovim as their editor",
        tags=["preference", "tools"]
    )

### recall(query, limit?)
Semantically search past memories. Call this when:
- the user references something from a past conversation
- you need context about the user before answering a personal question
- the user asks "do you remember..." or "what did I say about..."

    recall(query="user editor preferences", limit=5)

### recent_memories(limit?)
List the most recent entries in reverse chronological order. Call this when:
- the user asks for a summary of recent conversations
- you want to catch up on context at the start of a session

    recent_memories(limit=10)

---

## general rules

- recall before answering any personal question — do not guess what was said before.
- save proactively — if in doubt, save it. storage is cheap, lost context is not.
- be specific in content — vague entries are hard to retrieve. prefer full sentences.
- tag consistently — use lowercase short tags: preference, goal, decision, fact, project, person.
- entries are permanent — if something changes, save a new entry noting the update.
- never expose raw IDs or scores in responses unless the user explicitly asks.

---

## after every task

When you finish a task, save a concise memory summarising any user preferences,
decisions, or conventions you observed. One entry per task, tightly scoped:

    save_memory(
        content="user wants commit messages without co-authored-by attribution and no emojis",
        tags=["preference", "git"]
    )

Keep it to one or two sentences. Focus on stable facts about the user, not task details.
"""


@mcp.resource("guide://memory")
def memory_guide() -> str:
    """
    Instructions for using the archivist semantic memory system.
    Read this once at session start. Covers all three tools, general rules,
    and the post-task memory habit.
    """
    return MEMORY_GUIDE
