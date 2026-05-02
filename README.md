# research-mode

Pi skill for systematic, repeatable online research with:
- grill-first scoping
- Firecrawl-first discovery/fetching
- fallback web fetch/search when Firecrawl fails or lacks coverage
- adaptive Quick / Standard / Deep tiers
- reusable artifacts: markdown brief, JSON evidence ledger, source inventory, query log

## Structure
- `SKILL.md` — main skill instructions
- `references/` — detailed playbook, grilling flow, output templates
- `scripts/` — artifact scaffolding, logging, deterministic tool routing

## Default behavior
1. Grill scope first
2. Classify research type
3. Pick tier if unspecified
4. Use Firecrawl first:
   - `/v1/search` for discovery
   - `/v1/scrape` for known URLs
   - `/v1/map` for domain scoping
   - `/v1/crawl` only for site-wide escalation
5. Fall back to generic web fetch/search only on:
   - technical failure
   - blocked or empty content
   - insufficient coverage for the needed source class
6. Save research artifacts
7. Return concise final synthesis

## Helper scripts
```bash
python scripts/init_artifact.py --topic "ai competitor analysis" --research-type competitor --tier standard
python scripts/log_research_step.py --artifact-dir runs/2026-05-02-ai-competitor-analysis --mode query --query "..."
python scripts/route_tool.py --intent discover --depth standard
```

## Notes
- This repo is both the git repo root and the skill directory.
- The skill is designed for Pi and can be loaded via its directory path.
