# Quant Research Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and validate a reusable `quant-research` skill that produces free-source, evidence-ledger-driven, asset-class-aware quantitative research dossiers.

**Architecture:** The skill package lives in `quant-research/`. `SKILL.md` contains the compact trigger and workflow; deeper methodology lives in `references/`; deterministic dossier creation and baseline quant analysis live in `scripts/quant_research.py`; tests verify schema, artifact creation, and quant calculations without network access.

**Tech Stack:** Markdown skill files, YAML metadata, Python standard library plus optional `pandas`, `matplotlib`, and `yfinance` when installed, `unittest` tests, Codex skill-creator validation scripts.

---

## File Structure

- Create `quant-research/SKILL.md`: concise procedural skill instructions and reference-loading rules.
- Create `quant-research/agents/openai.yaml`: UI metadata for Codex skill lists.
- Create `quant-research/references/evidence-ledger.md`: evidence standards, source ranking, claim handling, and confidence rules.
- Create `quant-research/references/source-playbook.md`: free source ladder and asset-class source suggestions.
- Create `quant-research/references/asset-class-playbooks.md`: branch guidance for equities, ETFs/funds, crypto, FX, commodities, rates/bonds, options, and situations.
- Create `quant-research/references/research-lenses.md`: portable analyst lenses such as bottlenecks, proof gates, catalysts, market structure, valuation, macro sensitivity, and disagreement.
- Create `quant-research/references/output-templates.md`: dossier structure, report outline, ledger schema, and chat summary format.
- Create `quant-research/scripts/quant_research.py`: CLI for creating dossiers, validating evidence ledgers, importing price CSVs, computing quant stats, and writing charts when optional packages exist.
- Create `tests/test_quant_research.py`: local tests for artifact creation, evidence validation, and quant calculations.
- Create `.gitignore`: ignore local research outputs, caches, and Python artifacts.

### Task 1: Package Skeleton

**Files:**
- Create: `quant-research/SKILL.md`
- Create: `quant-research/agents/openai.yaml`
- Create: `.gitignore`

- [ ] **Step 1: Create the package directories**

Run: `New-Item -ItemType Directory -Force -Path 'quant-research','quant-research\agents','quant-research\references','quant-research\scripts','tests'`
Expected: directories exist with no errors.

- [ ] **Step 2: Write `SKILL.md`**

Create `quant-research/SKILL.md` with frontmatter:

```yaml
---
name: quant-research
description: Free-source quantitative investment research workflow for analyzing stocks, ETFs, crypto, commodities, FX, rates, options, funds, sectors, catalysts, and market situations. Use when Codex needs to build or refresh an evidence-ledger-backed research dossier with quantitative analysis, valuation or implied-expectations work, scenarios, proof gates, risks, monitoring triggers, and cited decision-support output without paid data.
---
```

Then include sections for: quick start, required workflow, research depths, evidence-first rules, artifact rules, quantitative script usage, reference-loading guide, non-advisory output, and verification checklist.

- [ ] **Step 3: Write `agents/openai.yaml`**

Create `quant-research/agents/openai.yaml`:

```yaml
display_name: Quant Research
short_description: Build evidence-ledger-backed quantitative research dossiers for assets and market situations using free sources.
default_prompt: Analyze this asset or market situation with a free-source, evidence-first quantitative research workflow. Create or refresh a local dossier, cite material claims, run reproducible quant analysis where data is available, and return a concise decision-support summary with artifact links.
```

- [ ] **Step 4: Write `.gitignore`**

Create `.gitignore` with:

```gitignore
__pycache__/
*.pyc
.pytest_cache/
research/
*.png
*.tmp
```

- [ ] **Step 5: Commit the skeleton**

Run: `git add .gitignore quant-research/SKILL.md quant-research/agents/openai.yaml && git commit -m "feat: add quant research skill skeleton"`
Expected: commit succeeds.

### Task 2: Reference Playbooks

**Files:**
- Create: `quant-research/references/evidence-ledger.md`
- Create: `quant-research/references/source-playbook.md`
- Create: `quant-research/references/asset-class-playbooks.md`
- Create: `quant-research/references/research-lenses.md`
- Create: `quant-research/references/output-templates.md`

- [ ] **Step 1: Write evidence standards**

Create `evidence-ledger.md` with a CSV schema:

```text
claim_id,claim,asset,source_type,source_name,source_url,source_date,access_date,evidence_excerpt,artifact_path,confidence,caveats,corroboration_status
```

Define allowed confidence values `high`, `medium`, `low`, and `unresolved`. Define source types `primary`, `regulatory`, `issuer`, `exchange`, `market_data`, `computed`, `secondary`, and `user_provided`.

- [ ] **Step 2: Write the source playbook**

Create `source-playbook.md` with the free-source ladder from the design. Include named examples such as SEC EDGAR, company IR pages, ETF sponsor pages, central banks, FRED, exchange pages, protocol documentation, CoinGecko or CoinMarketCap for crypto leads, Yahoo Finance or Stooq for free market data leads, and reputable news/search results as secondary sources.

- [ ] **Step 3: Write asset-class playbooks**

Create `asset-class-playbooks.md` with separate sections for equities, ETFs/funds, crypto, commodities, FX, rates/bonds, options, and situations. Each section lists required checks, common data gaps, appropriate valuation/implied-expectations methods, quant checks, and monitoring triggers.

- [ ] **Step 4: Write research lenses**

Create `research-lenses.md` with reusable procedures for bottleneck mapping, right-security tests, proof gates, catalysts, quant profile, market structure, macro sensitivity, valuation after rerating, disagreement ledger, and monitoring loop.

- [ ] **Step 5: Write output templates**

Create `output-templates.md` with the dossier tree, report outline, update memo outline, evidence ledger row examples, `asset-profile.json` schema, `analysis-manifest.json` schema, and concise chat summary format.

- [ ] **Step 6: Commit the references**

Run: `git add quant-research/references && git commit -m "docs: add quant research playbooks"`
Expected: commit succeeds.

### Task 3: Deterministic Research Script

**Files:**
- Create: `quant-research/scripts/quant_research.py`

- [ ] **Step 1: Implement CLI structure**

Create `quant_research.py` with subcommands:

```text
init-dossier --asset ASSET --asset-type TYPE --root research
validate-ledger --ledger PATH
analyze-prices --prices PATH --out-dir PATH --benchmark PATH
```

Use `argparse`, `csv`, `json`, `statistics`, `datetime`, and `pathlib` from the standard library.

- [ ] **Step 2: Implement dossier creation**

`init-dossier` creates the dossier tree from the design, writes `asset-profile.json`, `analysis-manifest.json`, `evidence-ledger.csv`, `source-registry.json`, `assumptions.md`, `limitations.md`, `watchlist-triggers.yaml`, and dated placeholder-free report path under `reports/`.

- [ ] **Step 3: Implement ledger validation**

`validate-ledger` checks required columns, allowed confidence values, allowed source types, non-empty claims, and non-empty source URL or artifact path for each row.

- [ ] **Step 4: Implement price analysis**

`analyze-prices` reads a CSV with `date` and `close`, sorts by date, computes total return, annualized volatility, max drawdown, best/worst daily return, positive-day ratio, and writes `quant-summary.json` and `returns.csv`.

- [ ] **Step 5: Implement optional charting**

If `matplotlib` is installed, write `price-chart.png` and `drawdown-chart.png`. If unavailable, skip charts and write the reason in `quant-summary.json`.

- [ ] **Step 6: Commit the script**

Run: `git add quant-research/scripts/quant_research.py && git commit -m "feat: add quant research helper script"`
Expected: commit succeeds.

### Task 4: Tests

**Files:**
- Create: `tests/test_quant_research.py`

- [ ] **Step 1: Write tests for dossier creation**

Test that running `init_dossier(asset="TEST", asset_type="equity", root=tempdir)` creates the required directories and files, and that JSON files contain the asset and asset type.

- [ ] **Step 2: Write tests for ledger validation**

Test that a valid ledger returns no errors. Test that a ledger missing `claim`, using confidence `certain`, or using source type `rumor` returns errors.

- [ ] **Step 3: Write tests for price analysis**

Use a fixed CSV of five prices. Assert total return, max drawdown, output files, and row count in `returns.csv`.

- [ ] **Step 4: Run tests**

Run: `python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 5: Commit tests**

Run: `git add tests/test_quant_research.py && git commit -m "test: cover quant research helper script"`
Expected: commit succeeds.

### Task 5: Skill Validation

**Files:**
- Modify: any skill file if validation finds defects.

- [ ] **Step 1: Run skill validation**

Run: `python C:\Users\fowle\.codex\skills\.system\skill-creator\scripts\quick_validate.py quant-research`
Expected: validation passes.

- [ ] **Step 2: Run script help smoke tests**

Run:

```powershell
python quant-research\scripts\quant_research.py --help
python quant-research\scripts\quant_research.py init-dossier --asset TEST --asset-type equity --root research-smoke
python quant-research\scripts\quant_research.py validate-ledger --ledger research-smoke\TEST\evidence-ledger.csv
```

Expected: help renders, dossier is created, and empty starter ledger validates.

- [ ] **Step 3: Remove smoke output**

Run: `Remove-Item -Recurse -Force research-smoke`
Expected: smoke output removed.

- [ ] **Step 4: Commit validation fixes**

If files changed, run: `git add quant-research tests && git commit -m "fix: satisfy quant research validation"`.

### Task 6: Forward Tests

**Files:**
- Create under ignored `research/` during tests.
- Modify skill references only if forward tests expose gaps.

- [ ] **Step 1: Test a liquid equity**

Use the skill manually on a liquid equity such as Microsoft or Nvidia at standard depth. Confirm it creates a dossier, evidence ledger entries, quant output from a price CSV or free retrieved data, and a decision-support summary without buy/sell language.

- [ ] **Step 2: Test a non-equity asset**

Use the skill manually on a major ETF or crypto asset. Confirm asset-class branching changes the analysis, valuation is asset-appropriate, and data gaps are explicit.

- [ ] **Step 3: Inspect artifacts**

Open the generated report, ledger, quant summary, and charts or chart-skip reason. Confirm they are internally consistent and trace claims back to evidence or computed artifacts.

- [ ] **Step 4: Patch defects**

If forward tests reveal missing instructions, edit `SKILL.md` or the relevant reference file with concrete guidance, rerun validation and tests, and commit with `git commit -m "fix: improve quant research workflow from forward test"`.

### Task 7: Completion Audit

**Files:**
- Inspect: `docs/superpowers/specs/2026-05-29-quant-research-skill-design.md`
- Inspect: `quant-research/`
- Inspect: test output and validation output.

- [ ] **Step 1: Verify spec coverage**

Map each spec section to implemented files and tests. Confirm asset coverage, evidence ledger, free source ladder, quant script, lenses, adaptive valuation, living dossiers, output contract, and validation requirements are present.

- [ ] **Step 2: Verify clean git state**

Run: `git status --short`
Expected: no unexpected tracked changes. Ignored `research/` forward-test outputs may remain ignored.

- [ ] **Step 3: Final response**

Report the created skill path, validation commands run, forward-test results, and any known limitations.
