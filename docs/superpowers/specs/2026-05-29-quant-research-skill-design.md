# Quant Research Skill Design

## Purpose

Build a reusable skill for Codex, Claude Code, and other skill-capable agents that performs rigorous, free-source, asset-class-aware investment research. The skill should help a user investigate securities and market situations with the feel of a disciplined PM/analyst team: evidence-first, quantitatively reproducible, skeptical, and capable of maintaining living research dossiers over time.

The skill must not behave like a stock-tip generator. Its default output is a decision-support framework: scenarios, evidence quality, proof gates, valuation/implied expectations, risks, monitoring triggers, and what would change the view.

## Scope

The skill supports as many assets and securities as possible, with analysis depth based on available free data:

- Public equities, ADRs, ETFs, funds, indexes, and major crypto assets.
- Commodities, FX pairs, rates, yields, and macro instruments when free data is available.
- Options, bonds, private companies, OTC securities, and obscure foreign assets with explicit caveats when data is incomplete.
- Company, sector, macro, catalyst, event, and portfolio/watchlist research questions.

The skill is code-capable by default. It assumes the agent can run local scripts for data retrieval, statistical analysis, charting, and artifact creation.

## Non-Goals

- Do not provide personalized financial advice or default to buy/sell/hold recommendations.
- Do not require paid data sources.
- Do not hide missing, stale, or inconsistent data behind confident prose.
- Do not make the first version sector-specific. Semiconductor and AI-infrastructure concepts should be generalized into portable research lenses.
- Do not paste an entire deep report into chat by default. The durable folder carries the full analysis.

## Core Workflow

Every run starts by classifying the request:

1. Identify the asset, security, or situation.
2. Determine the asset class, trading venue, identifiers, currency, and available free data.
3. Choose a depth: brief, standard, or deep. Default to standard when unspecified.
4. Decide whether this is initial coverage or a refresh of an existing dossier.
5. Create or update a local research folder.
6. Build or update the evidence ledger before making material claims.
7. Run quantitative analysis with local scripts where data permits.
8. Apply relevant research lenses.
9. Produce a decision framework and monitoring plan.
10. Return a concise executive summary with links to artifacts.

## Research Depths

Brief runs identify the asset, collect core facts, run basic price and return statistics when possible, summarize key risks and catalysts, cite sources, and list research gaps.

Standard runs create the full evidence ledger, quant profile, fundamentals or asset-specific equivalent, valuation or implied expectations, scenarios, proof gates, market-structure checks, and monitoring triggers.

Deep runs expand the source sweep, peer or comparable analysis, richer quantitative tests, historical analogs, disagreement analysis, valuation sensitivities, and unresolved diligence queue.

All depths must obey the evidence rules. Brief mode reduces scope, not rigor.

## Dossier Structure

Each investigated asset or situation gets a timestamped or canonical research folder, such as:

```text
research/
  NVDA/
    asset-profile.json
    analysis-manifest.json
    evidence-ledger.csv
    source-registry.json
    assumptions.md
    limitations.md
    watchlist-triggers.yaml
    source-notes/
    data/
    charts/
    quant/
    valuation/
    reports/
      2026-05-29-initial-report.md
      2026-08-30-earnings-refresh.md
```

The folder is a living dossier. Refreshes reuse existing state, ingest new filings, earnings, price data, news, or user-provided material, and append update memos instead of starting over.

## Evidence Ledger

The evidence ledger is the spine of the workflow. Every material claim must trace to one or more ledger entries or computed artifacts.

Each ledger entry should capture:

- Claim or data point.
- Source URL, file path, or document identifier.
- Source type: primary, regulatory, issuer, market data, secondary, user-provided, or computed.
- Publication date when available.
- Access date.
- Relevant excerpt, field, or calculation reference.
- Confidence level.
- Caveats.
- Corroboration status.

Unsupported claims are excluded from the main conclusion or explicitly marked unresolved.

## Free Source Ladder

The skill uses a tiered fallback model:

1. Primary, regulatory, issuer, exchange, central bank, fund sponsor, or protocol sources.
2. Official filings, investor relations material, earnings releases, transcripts, and fact sheets.
3. Free market-data APIs or downloadable datasets.
4. Reputable free financial portals.
5. News, search results, blogs, newsletters, social posts, and analyst commentary.
6. User-provided data.
7. If data remains unavailable, mark the gap and reduce confidence.

Secondary commentary can generate leads, but it is not proof unless corroborated by stronger evidence.

## Quantitative Analysis

The skill should include deterministic scripts for repeatable analysis:

- Historical prices and returns.
- Volatility, drawdown, rolling return, and momentum statistics.
- Correlation and beta against relevant benchmarks.
- Simple factor proxies where appropriate.
- Liquidity and volume profile.
- Event windows when dates are supplied.
- Charts and machine-readable output tables.

The agent should not eyeball figures from web pages when code can fetch, normalize, and compute them reproducibly.

## Research Lenses

The core skill includes portable lenses that can apply across asset classes:

- Bottleneck or constraint mapping: identify the scarce input, bottleneck, regulation, balance-sheet constraint, liquidity condition, or adoption hurdle that controls the outcome.
- Right-security test: decide whether the selected security is the cleanest expression of the thesis.
- Proof gates: define observable events that validate, advance, or invalidate the thesis.
- Catalyst map: scheduled and unscheduled events plus expected market interpretation.
- Quant/statistical profile: return behavior, volatility, drawdowns, correlations, factors, and regime sensitivity.
- Market-structure overlay: liquidity, float or supply, ownership, dilution/unlocks, short interest, borrow, flows, index inclusion, or equivalent asset-specific mechanics.
- Macro sensitivity: rates, inflation, FX, commodities, liquidity, credit spreads, policy, and risk appetite.
- Valuation and implied expectations: determine what must happen for current pricing to make sense.
- Disagreement ledger: identify where credible sources, narratives, or data conflict and convert disagreement into diligence tasks.
- Monitoring loop: define what to refresh, how often, and what changes matter.

## Valuation and Implied Expectations

Valuation is adaptive:

- Equities: multiples, historical ranges, peer comparison, implied expectations, and DCF only when data and assumptions justify it.
- ETFs and funds: holdings, expense ratio, exposure, tracking behavior, distributions, NAV/premium-discount where relevant.
- Crypto, commodities, and FX: supply/demand, flows, macro sensitivity, market structure, and protocol or on-chain proxies where freely available.
- Options: payoff, implied volatility, and Greeks only when reliable free chain data is available.
- Bonds and rates: yield, duration, credit risk, inflation/rate sensitivity, issuer and structure caveats.

The skill must separate "good thesis" from "still attractive setup" after rerating.

## Output Contract

Chat output is an executive summary:

- What was analyzed.
- Current decision framework.
- Most important evidence.
- Base/bull/bear or equivalent scenarios.
- Key risks, proof gates, and invalidation signals.
- Monitoring triggers.
- Major data gaps and confidence level.
- Links to the research folder, final report, evidence ledger, charts, and data artifacts.

The full report lives in the dossier.

## Skill Package Design

Use one main skill folder with:

```text
quant-research/
  SKILL.md
  agents/
    openai.yaml
  scripts/
    quant_research.py
  references/
    evidence-ledger.md
    source-playbook.md
    asset-class-playbooks.md
    research-lenses.md
    output-templates.md
```

`SKILL.md` stays concise and procedural. Detailed guidance lives in references so agents load only what they need.

The first script should provide reliable local artifact creation and baseline quant analysis. It should work without paid credentials and produce clear failure messages when free data is missing.

## Validation

The completed skill must pass:

- Skill structure validation with the skill creator validation script.
- Script help or smoke tests.
- At least one realistic forward test against a liquid public equity.
- At least one realistic forward test against a non-equity asset such as a major crypto asset or ETF.
- Artifact inspection to confirm the dossier, evidence ledger, report, data, and charts are created or updated.

Forward tests should verify that the skill produces decision-support analysis with citations and caveats, not unsupported recommendations.
