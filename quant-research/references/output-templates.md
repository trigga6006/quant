# Output Templates

## Dossier Tree

```text
research/
  <ASSET>/
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
      YYYY-MM-DD-initial-report.md
      YYYY-MM-DD-refresh.md
```

## Initial Report Outline

```markdown
# <Asset> Research Dossier

## Executive Summary

## Asset Identification

## Evidence Quality and Data Gaps

## Quantitative Profile

## Fundamental, Structural, or Protocol Analysis

## Crypto Contract, Tokenomics, and On-Chain Analysis

Use when the asset is a crypto token, protocol, smart contract, wallet, mint, DAO, pool, bridge, or yield product.

```markdown
## Protocol Identity and Address Resolution

## Cross-Chain Deployment Matrix

## Investment Diligence

## Tokenomics, Emissions, and Unlocks

## Smart Contract / Security Review

## Scam and Rug Risk Screen

## On-Chain Forensics

## Audit Coverage

## Crypto Risk Buckets
```

## Partnerships and Ecosystem Dependencies

## Bottleneck and Constraint Map

## Valuation or Implied Expectations

## Scenarios

## Proof Gates and Invalidation Signals

## Catalyst Calendar and Monitoring Plan

## Market Structure

## Macro Sensitivity

## Disagreement and Diligence Queue

## Limitations
```

## Refresh Memo Outline

```markdown
# <Asset> Refresh Memo - YYYY-MM-DD

## What Changed

## Evidence Added

## Partnership, Ecosystem, and Bottleneck Changes

## Quantitative Changes

## Scenario Updates

## Proof Gates and Trigger Status

## New Risks or Resolved Risks

## Updated Monitoring Plan

## Remaining Questions
```

## Asset Profile JSON

```json
{
  "asset": "NVDA",
  "asset_type": "equity",
  "canonical_name": "",
  "identifiers": {},
  "venue": "",
  "currency": "",
  "benchmark": "",
  "created_at": "2026-05-29T00:00:00Z",
  "last_updated": "2026-05-29T00:00:00Z"
}
```

## Analysis Manifest JSON

```json
{
  "asset": "NVDA",
  "depth": "standard",
  "mode": "initial",
  "created_at": "2026-05-29T00:00:00Z",
  "last_updated": "2026-05-29T00:00:00Z",
  "reports": [],
  "data_artifacts": [],
  "quant_artifacts": [],
  "valuation_artifacts": [],
  "known_gaps": []
}
```

## Evidence Ledger Row Example

```csv
claim_id,claim,asset,source_type,source_name,source_url,source_date,access_date,evidence_excerpt,artifact_path,confidence,caveats,corroboration_status
NVDA-001,Nvidia reported data center revenue for the quarter,NVDA,issuer,Nvidia investor relations,https://example.com,2026-05-01,2026-05-29,Data center revenue line item,,high,Verify against 10-Q when filed,single_source
```

## Chat Executive Summary

```markdown
**Analyzed:** <asset/situation> at <brief|standard|deep> depth.

**Decision Framework:** <one paragraph>

**Evidence:** <3-5 sourced or computed points>

**Scenarios:** Base: <...>. Bull: <...>. Bear: <...>.

**Crypto Contract / On-Chain:** <address confidence, security bucket, tokenomics bucket, on-chain forensic bucket, and major unresolved contract risks if relevant>

**Partnerships and Bottlenecks:** <validated relationships, dependencies, constraints, and weak/unproven claims>

**Proof Gates:** <events or data that would validate/invalidate>

**Catalysts and Monitoring:** <dated events, quality grade, and what to watch after>

**Confidence and Gaps:** <confidence level plus missing/stale data>

**Artifacts:** [dossier](path), [report](path), [ledger](path), [quant summary](path)
```
