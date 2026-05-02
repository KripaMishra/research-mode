---
name: research-mode
description: Use when a task needs systematic online research with scope clarification, source discovery, iterative expansion, competitor or market exploration, or a reusable evidence trail. Best for market analysis, competitor analysis, exploratory analysis, and non-trivial topic research where Firecrawl should be tried first and final synthesis must be auditable.
---

# Research Mode

## Purpose
Bounded, auditable research loop: **grill → classify → discover → expand → saturate → synthesize**

**Firecrawl MCP tools first.** Fall back to generic web tools only when Firecrawl fails or coverage is insufficient.

## When to use
- Multiple searches or source comparisons needed
- Market, competitor, exploratory, or broad topic research
- Needs reusable evidence trail and source inventory

Do **not** use for trivial single-fact lookups.

## Hard rules
1. **Grill first** — no searching before scope is locked
2. **Firecrawl first** — use MCP tools before falling back
3. **Log fallbacks** — always record why Firecrawl was insufficient
4. **Evidence-only synthesis** — final answer must not outrun captured evidence
5. **Concise final response** — deep process, compact presentation

## Tool routing
Use in this order:

| Intent | Tool | Fall back when |
|---|---|---|
| Topic discovery | `search(query, limit=5)` | technical failure, empty/blocked, insufficient coverage |
| Known URL | `scrape(url)` | technical failure, blocked/empty |
| Domain URL inventory | `map_site(url)` | technical failure |
| Site-wide indexing | `crawl_start(url)` → `crawl_status(job_id)` | technical failure |
| Fallback | `web_search` + `fetch_content` | only after Firecrawl fails |

## Start-of-run protocol
1. Read `references/grill-question-flow.md`
2. Ask grilling questions one at a time (numbered MCQ format, see reference)
3. Lock: objective, deliverable, research type, tier
4. Initialize artifacts:
```bash
python scripts/init_artifact.py --topic "<topic>" --research-type <market|competitor|exploratory|simple-topic> --tier <quick|standard|deep>
```

## Research types
- **market**: category → segments → size → demand proxies → constraints
- **competitor**: direct → indirect → substitute; pricing / docs / reviews / job posts / release notes
- **exploratory**: concept map → source map → gap map → synthesis
- **simple-topic**: canonical answer → verify → caveat

## Tiers
| Tier | Queries | Pages | Expansion passes |
|---|---|---|---|
| Quick | 3–5 | 5–10 | 1 |
| Standard | 6–10 | 10–20 | 2–3 |
| Deep | 10–20 | 20–40 | 3–5 |

Budgets are soft defaults — adjust with rationale and log the change.

## Core loop

### 1. Discover broadly
- Multiple query phrasings, varied terminology, adjacent terms, time windows
- Log each query:
```bash
python scripts/log_research_step.py --artifact-dir <dir> --mode query \
  --query "..." --intent discover --tool search
```

### 2. Evaluate sources
- Official/primary > independent secondary > behavioral traces
- Use lateral reading on unfamiliar sources before trusting them

### 3. Expand
- Follow citations, direct/indirect/substitute entities, adjacent concepts
- Log each source:
```bash
python scripts/log_research_step.py --artifact-dir <dir> --mode source \
  --url "..." --title "..." --source-class primary
```
- Log each claim:
```bash
python scripts/log_research_step.py --artifact-dir <dir> --mode evidence \
  --claim "..." --url "..." --confidence high --note "..."
```

### 4. Stop when
- 2 consecutive passes with no new source family and no materially new claims
- Novelty yield drops below ~10–15%
- Each major claim has primary/official support where available

### 5. Fallback logging
```bash
python scripts/log_research_step.py --artifact-dir <dir> --mode fallback \
  --source firecrawl --reason "blocked page" --details "scrape returned empty markdown"
```

Valid reasons: timeout, 4xx/5xx, blocked/empty content, insufficient coverage, unsupported need.

## Artifacts (saved to `./runs/`)
- `brief.md` — working brief and final synthesis
- `evidence.json` — structured evidence ledger
- `sources.json` — source inventory
- `queries.json` — query/search log
- `meta.json` — run metadata

## Subagent policy
- **Quick**: single-agent unless scope expands
- **Standard**: consider for independent research angles
- **Deep**: strongly consider subagents

Good splits: official sources / market landscape / contradictions / local vs external context

## Final response
```md
## Answer
[short synthesis]

## Key evidence
- [claim] — [source]

## Caveats
- [gap or contradiction]

## Raw artifact
Saved to: `path`
```

Use richer templates from `references/final-output-templates.md` for market/competitor/exploratory tasks.

## Common mistakes
- Searching before grilling
- Using fallback tools before trying Firecrawl
- Treating one search page as exhaustive
- Not logging fallback reasons
- Polished answer without evidence trail
- Forcing conclusion when evidence is thin
