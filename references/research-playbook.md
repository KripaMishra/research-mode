# Research playbook

## Core model
Run research as:

**scope -> decompose -> discover -> evaluate -> expand -> saturate -> synthesize**

This skill treats “exhaustive” as:
- systematic
- repeatable
- source-class aware
- explicit about gaps
- stopped by diminishing returns, not by guesswork

## Source-class coverage model
Prefer coverage across source classes, not just many URLs.

1. **Official / primary**
   - company docs
   - pricing pages
   - product docs
   - filings
   - standards
   - government datasets
   - first-party reports

2. **Independent / secondary**
   - analyst pieces
   - reputable trade press
   - secondary research writeups
   - academic surveys and reviews

3. **Behavioral traces**
   - reviews
   - customer discussions
   - job posts
   - release notes
   - changelogs
   - social activity
   - marketplace listings

4. **Network expansion**
   - citations
   - references
   - related vendors
   - substitutes
   - adjacent concepts or segments

## Firecrawl-first tool order
Based on the local Firecrawl proxy workflow:

1. `/v1/search`
   - best first move for topic discovery
   - use it when you do not yet know the best URLs

2. `/v1/scrape`
   - use when you already know the important URL

3. `/v1/map`
   - use when you need a domain inventory before picking pages

4. `/v1/crawl`
   - use only for site-wide escalation
   - not the normal default

Fallback to generic web tools only when Firecrawl cannot do the job well enough.

## Discovery strategy
Start broad and branch intentionally.

### Broad discovery
- vary wording
- vary entity names
- vary levels of abstraction
- vary date windows if recency matters
- query for source classes, not just topics

### Expansion heuristics
Expand through:
- backward citations
- forward citations
- named references on high-signal pages
- direct -> indirect -> substitute competitors
- adjacent segments or related terms
- contradictions or suspicious claims
- missing source classes

## Reliability rules
- prefer primary sources for high-stakes claims
- use secondary sources for synthesis and interpretation
- lateral-read unfamiliar domains before trusting them
- preserve contradictions; do not smooth them away
- do not cite a source you did not inspect

## Suggested stop rules
Default stop when all are true:
- 2 consecutive iterations add no new source family and no materially new claim
- novelty yield in the last pass is low (~10-15%)
- major claims have primary/official support where available
- required source classes have been covered

If one of these is false, continue or report the gap explicitly.

## Branch guides

### Market analysis
Path:
- category -> segments -> market size inputs -> demand proxies -> constraints -> notable players

Good source mix:
- official data
- independent analysis
- search trend / reviews / forums / hiring demand proxies

### Competitor analysis
Path:
- direct -> indirect -> substitutes -> product/pricing/positioning -> reviews -> launch/hiring/distribution signals

Good source mix:
- competitor sites
- pricing pages
- docs
- release notes
- job posts
- review platforms
- earned media

### Exploratory analysis
Path:
- concept map -> source map -> theme map -> contradiction map -> concise synthesis

Good source mix:
- canonical explainers
- landmark papers/docs
- secondary synthesis
- citation network

### Simple topic research
Path:
- canonical answer -> one independent verification -> caveat

Good source mix:
- official docs
- one or two trustworthy independent checks

## Evidence ledger shape
Each evidence row should capture:
- claim
- source title
- URL
- source class
- date accessed
- excerpt or datapoint
- interpretation
- confidence
- caveat or contradiction
- tags

## Query log shape
Each query log entry should capture:
- timestamp
- query
- intent
- tool chosen
- why that tool was chosen
- fallback reason if any
- short result summary
