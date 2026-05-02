---
name: research-mode
description: Use when a task needs systematic online research with scope clarification, source discovery, iterative expansion, competitor or market exploration, or a reusable evidence trail. Best for market analysis, competitor analysis, exploratory analysis, and non-trivial topic research where Firecrawl should be tried first and final synthesis must be auditable.
---

# Research Mode

## Purpose
Run research as a bounded, auditable loop:

**grill -> classify -> tier -> discover -> extract -> expand -> saturate -> synthesize**

Default to **Firecrawl first**. Use generic web search/fetch only when Firecrawl fails technically or cannot provide enough useful coverage.

## Read these references when needed
- Read `references/grill-question-flow.md` at the start of each run.
- Read `references/research-playbook.md` when planning or executing the research loop.
- Read `references/final-output-templates.md` before drafting the final answer.

## When to use
Use this skill when:
- the user wants more than a one-shot lookup
- the task needs multiple searches or source comparisons
- the task needs market analysis, competitor analysis, exploratory analysis, or broad topic research
- the answer needs a reusable evidence ledger and source inventory
- the user wants systematic or exhaustive research, not just a quick answer

Do **not** use this skill for trivial single-fact lookups unless the user explicitly asks for the research workflow.

## Hard rules
1. **Always grill first.** Do not start searching before a short scope-confirmation pass.
2. **Firecrawl first.** Prefer Firecrawl for discovery and page retrieval.
3. **Fallback only with a reason.** When falling back, log why Firecrawl was insufficient.
4. **Log the trail.** Save query log, source inventory, and evidence ledger.
5. **Synthesize only from captured evidence.** Do not let the final answer outrun the evidence notes.
6. **Be concise in the final response.** Research process can be deep; presentation should stay compact.

## Start-of-run protocol
1. Read `references/grill-question-flow.md`.
2. Ask the minimum grilling questions needed to lock scope.
3. Infer the research type and tier if not specified, then confirm with the user.
4. If the request is too broad, decompose it into branches and ask the user to confirm the first branch.
5. Initialize artifacts with:
```bash
python scripts/init_artifact.py --topic "<topic>" --research-type <market|competitor|exploratory|simple-topic> --tier <quick|standard|deep>
```
6. Use `python scripts/route_tool.py ...` whenever tool choice is ambiguous.

## Research type defaults
- **market**: category -> segments -> size -> demand proxies -> constraints
- **competitor**: direct -> indirect -> substitute competitors; pricing/docs/reviews/job posts/release notes
- **exploratory**: concept map -> source map -> gap map -> synthesis
- **simple-topic**: canonical answer -> verify -> caveat

## Tier defaults
If the user does not specify a tier, infer one and confirm.

### Quick
- soft budget: 3-5 discovery queries
- 5-10 high-signal pages
- 1 expansion pass
- usually no subagents unless scope broadens

### Standard
- soft budget: 6-10 discovery/expansion queries
- 10-20 pages
- 2-3 expansion passes
- may use subagents for parallel research angles

### Deep
- soft budget: 10-20 queries
- 20-40 pages or targeted domain follow-up
- 3-5 expansion passes
- strongly consider subagents

Budgets are **soft defaults**. Adjust only with rationale and log the change.

## Firecrawl-first routing
Use this order by default:

1. **Discovery** -> Firecrawl `/v1/search`
2. **Known important URL** -> Firecrawl `/v1/scrape`
3. **Need domain URL inventory before follow-up** -> Firecrawl `/v1/map`
4. **Need site-wide indexing or broad domain harvesting** -> Firecrawl `/v1/crawl`
5. **Fallback** -> generic web search/fetch tools only if Firecrawl fails or coverage is inadequate

Use the helper for deterministic routing:
```bash
python scripts/route_tool.py --intent discover --depth standard
python scripts/route_tool.py --intent fetch --url https://example.com
python scripts/route_tool.py --intent domain-scope --url https://example.com
```

## Valid fallback reasons
Fallback is allowed only when one of these is true:
- Firecrawl technical failure: timeout, 4xx/5xx, malformed response
- blocked or empty page content
- no useful search results for the needed subquestion
- insufficient coverage for a required source class
- unsupported need that requires a non-Firecrawl tool

Whenever fallback happens, log it:
```bash
python scripts/log_research_step.py --artifact-dir <dir> --mode fallback \
  --source firecrawl --reason "blocked page" --details "search succeeded but scrape returned empty markdown"
```

## Core loop
### 1) Grill
Use `references/grill-question-flow.md`.
Keep questions short. Lock:
- objective
- deliverable
- research type
- tier
- required source classes
- geography/time horizon if relevant
- stopping conditions if user has special requirements

### 2) Initialize and log
Create artifacts with `init_artifact.py`.
Log each query, source, evidence item, and fallback with `log_research_step.py`.

### 3) Discover broadly
Start broad, then narrow.
- Use multiple query phrasings
- vary terminology, entities, adjacent terms, and time windows
- cover source classes, not just URLs

### 4) Evaluate sources
Prefer:
- official/primary sources for major claims
- independent secondary sources for interpretation
- behavioral traces for market/competitor signals

Use lateral reading on unfamiliar sources before trusting them.

### 5) Expand from discovery
Expand through:
- citations/references
- direct -> indirect -> substitute entities
- related concepts / adjacent segments
- unresolved contradictions
- source-class gaps

### 6) Stop with explicit rules
Default stop rules:
- 2 consecutive iterations with no new source family and no materially new claims
- novelty yield drops below ~10-15%
- each major claim has primary/official support where available
- required source classes are covered

If the next pass is likely to repeat covered ground, stop and report gaps.

### 7) Synthesize
Before writing the final answer, read `references/final-output-templates.md`.
Assemble only from verified evidence notes.
Preserve contradictions and caveats.

## Artifact expectations
Each run should produce:
- `brief.md` — working brief and final synthesis
- `evidence.json` — structured evidence ledger
- `sources.json` — source inventory
- `queries.json` — raw query/search log
- `meta.json` — run metadata

Default output root is `./runs/`. Override with `--output-root` when needed.

## Subagent policy
Subagents are optional, not mandatory.

- **Quick**: usually single-agent unless scope expands
- **Standard**: consider subagents for independent research angles
- **Deep**: strongly consider subagents

When unclear, ask the user first or state the recommendation before launching.

Good parallel splits:
- official / primary sources
- market or competitor landscape
- contradictions / validation pass
- local context vs external evidence when combined with repo work

## Final response rule
Keep the chat response concise. Default to:
```md
## Answer
[short synthesis]

## Key evidence
- [claim] — [source]
- [claim] — [source]

## Caveats
- [gap or contradiction]

## Raw artifact
Saved to: `path-or-obsidian-link`
```

Use the richer templates from `references/final-output-templates.md` when the task needs market/competitor/exploratory sections.

## Example flow
```bash
python scripts/init_artifact.py --topic "AI code review competitors" --research-type competitor --tier standard
python scripts/route_tool.py --intent discover --depth standard
python scripts/log_research_step.py --artifact-dir runs/2026-05-02-ai-code-review-competitors --mode query --query "AI code review competitors pricing"
python scripts/log_research_step.py --artifact-dir runs/2026-05-02-ai-code-review-competitors --mode source --url https://example.com --title "Example" --source-class primary
python scripts/log_research_step.py --artifact-dir runs/2026-05-02-ai-code-review-competitors --mode evidence --claim "Vendor X uses seat-based pricing" --url https://example.com/pricing --confidence high --note "Pricing page shows annual seat tiers"
```

## Common mistakes
- starting to search before grilling
- using generic web tools before Firecrawl
- treating one search page as exhaustive coverage
- failing to log fallback reasons
- writing a polished answer without a reusable evidence trail
- forcing a conclusion when the evidence is contradictory or thin
