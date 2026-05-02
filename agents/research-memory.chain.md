---
name: research-memory
description: Research with persistent memory — retrieves past findings, researches gaps via web search, saves distilled knowledge to memory
---

## memory-reader
output: memory-context.md

Retrieve past findings on the research topic.
1. Call `mcp({ search: "search" })` to find the memory search tool
2. Search with the topic keywords
3. Write memory-context.md: list any relevant past findings with source URLs, or write "No prior findings." if empty

## researcher
reads: memory-context.md
output: research.md

Research the topic following your standard process.
If memory-context.md contains prior findings, focus your searches on gaps not already covered — skip re-searching what's known.

## worker
reads: research.md
output: false

Save research findings to persistent memory.
1. Read research.md
2. Call `mcp({ search: "save" })` to find the save_observation tool
3. Save with:
   - title: the research topic
   - content: top 5–7 findings with source URLs
   - type: "project" if implementation-relevant, "reference" otherwise
