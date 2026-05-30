---
name: quant-research
description: Free-source quantitative investment research workflow for analyzing stocks, ETFs, crypto, commodities, FX, rates, options, funds, sectors, catalysts, portfolios, watchlists, and market situations. Use when Codex needs to create or refresh an evidence-ledger-backed research dossier with reproducible quantitative analysis, valuation or implied-expectations work, scenarios, proof gates, risks, monitoring triggers, and cited decision-support output without paid data.
---

# Quant Research

## Core Posture

Act like a skeptical research team, not a stock-tip generator. Build a decision-support framework with evidence, scenarios, uncertainty, proof gates, and monitoring triggers. Do not default to buy/sell/hold recommendations or personalized financial advice.

Use only free or user-provided sources unless the user explicitly supplies paid data. If data is missing, stale, blocked, or inconsistent, say so and lower confidence.

## Quick Start

1. Classify the request as initial coverage, refresh, comparison, portfolio/watchlist work, event analysis, or focused follow-up.
2. Identify the asset or situation: ticker/name, asset class, venue, currency, identifiers, relevant benchmark, and available free data.
3. Choose depth: `brief`, `standard`, or `deep`. Default to `standard`.
4. Create or update a local dossier with `scripts/quant_research.py init-dossier`.
5. Build or update `evidence-ledger.csv` before making material claims.
6. Run code-backed quantitative analysis when usable price data is available.
7. Load only the reference files needed for the asset class and research question.
8. For standard or deep work, explicitly test whether partnerships, ecosystem dependencies, bottlenecks, or catalysts are material to the thesis.
9. Produce a concise chat executive summary with links to the dossier artifacts.

## Research Depths

- `brief`: core identity, basic source check, basic price/return stats when available, key risks/catalysts, evidence gaps.
- `standard`: full evidence ledger, quant profile, asset-appropriate fundamentals, partnership/ecosystem check, valuation or implied expectations, scenarios, proof gates, market structure, monitoring triggers.
- `deep`: broader source sweep, peer/comparable work, richer quant tests, historical analogs, partnership economics, bottleneck map, catalyst calendar, disagreement analysis, valuation sensitivities, and a diligence queue.

Brief mode reduces claim count and source breadth. It does not relax citation or caveat standards.

## Required Dossier

Create a living dossier under `research/<asset-or-situation>/` unless the user asks for a different path. Refresh runs must reuse existing state, ingest changes, append update memos, and preserve prior evidence.

The standard dossier files are:

- `asset-profile.json`
- `analysis-manifest.json`
- `evidence-ledger.csv`
- `source-registry.json`
- `assumptions.md`
- `limitations.md`
- `watchlist-triggers.yaml`
- `source-notes/`
- `data/`
- `charts/`
- `quant/`
- `valuation/`
- `reports/`

Use:

```bash
python quant-research/scripts/quant_research.py init-dossier --asset NVDA --asset-type equity --root research
```

## Evidence Rules

Every material claim must trace to `evidence-ledger.csv` or a computed artifact. Unsupported claims belong in gaps, unresolved questions, or caveats, not in conclusions.

Read `references/evidence-ledger.md` before doing standard or deep research, any refresh, or any work where source quality matters.

Use this source ladder:

1. Primary, regulatory, issuer, exchange, central bank, fund sponsor, or protocol sources.
2. Filings, investor relations material, earnings releases, transcripts, and fact sheets.
3. Free market-data APIs or downloadable datasets.
4. Reputable free financial portals.
5. News, search results, blogs, newsletters, social posts, and analyst commentary.
6. User-provided data.
7. If data remains unavailable, mark the gap and reduce confidence.

Secondary commentary may generate leads, but it is not proof unless corroborated by stronger evidence.

## Quantitative Work

Prefer reproducible calculations over eyeballing web pages. For local price CSVs with `date` and `close`, run:

```bash
python quant-research/scripts/quant_research.py analyze-prices --prices path/to/prices.csv --out-dir research/NVDA/quant
```

The script writes summary statistics, returns, and charts when optional charting dependencies are installed. If free data cannot be retrieved or normalized, document the gap in `limitations.md` and the final summary.

## Reference Loading

Load references progressively:

- `references/output-templates.md`: when creating reports, update memos, ledger rows, or chat summaries.
- `references/source-playbook.md`: when choosing free sources or fallback sources.
- `references/asset-class-playbooks.md`: when branching by asset class.
- `references/research-lenses.md`: when applying partnership/ecosystem, bottleneck, catalyst, market-structure, macro, valuation, disagreement, or monitoring analysis.
- `references/evidence-ledger.md`: whenever claims, citations, confidence, or validation matter.

## Analysis Requirements

For standard or deep work, cover:

- Asset identification and data availability.
- Quant/statistical profile.
- Asset-appropriate fundamental, structural, or protocol analysis.
- Strategic partnerships, ecosystem dependencies, customer/supplier concentration, and bottleneck exposure when relevant.
- Valuation or implied expectations when applicable.
- Base, bull, and bear scenarios or asset-appropriate equivalents.
- Proof gates, invalidation signals, and catalyst quality.
- Catalyst calendar and monitoring triggers.
- Market-structure mechanics where relevant.
- Macro sensitivity where relevant.
- Disagreement ledger and unresolved diligence queue.
- Explicit limitations and confidence level.

## Refresh Workflow

When a dossier already exists:

1. Read `analysis-manifest.json`, `asset-profile.json`, `source-registry.json`, and the latest report.
2. Identify what changed since the last run: price, filings, earnings, macro data, news, partnerships, customer/supplier evidence, bottlenecks, source views, catalysts, proof gates, and watchlist triggers.
3. Add new evidence rows instead of overwriting old rows.
4. Write a dated update memo in `reports/`.
5. Update `watchlist-triggers.yaml`, assumptions, limitations, and manifest timestamps.

## Output Contract

Return a concise executive summary in chat:

- What was analyzed and at what depth.
- Current decision framework.
- Most important evidence.
- Scenarios and what would change them.
- Key risks, partnerships/ecosystem dependencies, bottlenecks, proof gates, and invalidation signals.
- Monitoring triggers.
- Major data gaps and confidence level.
- Links to the dossier, report, evidence ledger, charts, and data artifacts.

Do not paste the whole deep report into chat unless the user asks.

## Verification

Before saying the work is complete, run applicable checks:

```bash
python quant-research/scripts/quant_research.py validate-ledger --ledger research/<asset>/evidence-ledger.csv
python -m unittest discover -s tests -v
python C:/Users/fowle/.codex/skills/.system/skill-creator/scripts/quick_validate.py quant-research
```

If a check cannot run, report exactly why and what evidence was still inspected.
