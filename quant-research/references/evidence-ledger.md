# Evidence Ledger

Use the evidence ledger as the audit trail for every material claim. If a claim cannot be tied to a ledger row or computed artifact, keep it out of the main conclusion.

## CSV Schema

```text
claim_id,claim,asset,source_type,source_name,source_url,source_date,access_date,evidence_excerpt,artifact_path,confidence,caveats,corroboration_status
```

Required fields:

- `claim_id`: stable short identifier such as `NVDA-2026-001`.
- `claim`: concise factual claim or data point.
- `asset`: ticker, identifier, or situation name.
- `source_type`: one of the allowed source types below.
- `source_name`: issuer, regulator, dataset, publication, or artifact name.
- `source_url`: source URL when web-based.
- `source_date`: publication or observation date when known.
- `access_date`: date the agent accessed the source.
- `evidence_excerpt`: short excerpt, table field, or data description.
- `artifact_path`: local path for computed or user-provided evidence.
- `confidence`: one of the allowed confidence values below.
- `caveats`: data-quality limitations or interpretation limits.
- `corroboration_status`: `single_source`, `corroborated`, `conflicting`, or `unresolved`.

At least one of `source_url` or `artifact_path` must be non-empty for each non-empty row.

## Allowed Source Types

- `primary`: direct company, protocol, issuer, or project source.
- `regulatory`: SEC, central bank, government, court, exchange regulator, or equivalent.
- `issuer`: fund sponsor, bond issuer, ETF factsheet provider, or company investor relations.
- `exchange`: official exchange, index provider, market operator, or listing venue.
- `market_data`: free price, volume, rates, macro, or instrument dataset.
- `computed`: locally generated statistic, chart, valuation table, or model output.
- `secondary`: news, blogs, newsletters, social posts, analyst commentary, or search results.
- `user_provided`: files, notes, exports, or instructions supplied by the user.

## Confidence Values

- `high`: primary/regulatory/computed evidence is recent, directly relevant, and corroborated or self-contained.
- `medium`: source is credible but indirect, dated, or only partly corroborated.
- `low`: secondary, stale, incomplete, or weakly corroborated evidence.
- `unresolved`: useful lead or open question that must not support a hard conclusion.

## Claim Handling Rules

Use primary and regulatory sources for hard facts when possible. Use secondary sources as leads unless corroborated. Record conflicting evidence explicitly instead of averaging it away.

For computed claims, record the local artifact path and describe the calculation. If a number depends on assumptions, put the assumptions in `assumptions.md` and link the artifact path.

If a source cannot be accessed, add the issue to `limitations.md`; do not invent substitute details.

## Validation

Run:

```bash
python quant-research/scripts/quant_research.py validate-ledger --ledger research/<asset>/evidence-ledger.csv
```

Fix schema, confidence, source type, empty claim, and missing evidence-location errors before relying on the ledger.
