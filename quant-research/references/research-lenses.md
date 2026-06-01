# Research Lenses

Apply lenses selectively. Use them to improve judgment, not to create unnecessary sections.

## Bottleneck or Constraint Mapping

Ask what scarce input or constraint controls the outcome: supply, capacity, regulation, balance-sheet funding, liquidity, technical capability, customer adoption, distribution, energy, labor, data, or trust.

Then ask who captures the economics of relieving that constraint and whether the selected security is actually exposed to it.

Build a bottleneck table for any material thesis:

```text
constraint | owner/controller | affected assets | beneficiary | evidence | durability | bypass risk | investable expression | proof gate | invalidation signal
```

Classify the bottleneck:

- `structural`: hard to solve because of physics, regulation, capital intensity, patents, network effects, trust, geography, or time.
- `cyclical`: driven by inventory, capacity, rates, funding, commodity cycle, or temporary demand/supply imbalance.
- `narrative`: widely discussed but weakly supported by primary evidence.
- `false`: real theme, wrong constraint, wrong beneficiary, or already bypassed.

Pressure-test bypass risk. Ask whether technology substitution, regulation, customer insourcing, new capacity, open-source alternatives, vertical integration, or cheaper substitutes can erode the constraint before the thesis pays off.

When the bottleneck comes from news or a market-moving development, combine this lens with `serenity-alpha-workflow.md`: demand must be observable, financial transmission must be clear, and the candidate must be small/pure enough for the bottleneck to matter in reported results.

## Strategic Partnerships and Ecosystem Map

Use this lens whenever the asset depends on customers, suppliers, distributors, hyperscalers, protocols, exchanges, channel partners, licensing, government awards, joint ventures, strategic investors, or named commercial relationships.

Do not treat partnership press releases as proof. Classify each relationship:

- `commercial`: purchase order, contracted revenue, usage-based revenue, backlog, take-or-pay, or renewal evidence.
- `technical`: integration, qualification, certification, reference design, standard support, or developer adoption.
- `distribution`: reseller, marketplace, cloud/channel access, exchange listing, custody access, broker platform, or geographic route-to-market.
- `supply`: capacity reservation, long-term supply agreement, prepayment, exclusivity, or critical input access.
- `financing`: strategic investment, loan, grant, prepayment, offtake financing, or balance-sheet support.
- `regulatory/government`: award, approval, framework agreement, procurement vehicle, reimbursement, license, or policy support.
- `marketing`: co-announcement, memorandum of understanding, non-binding pilot, logo slide, or vague collaboration.

For each material partner, capture:

```text
partner | relationship_type | evidence_source | signed_or_nonbinding | economics_visible | exclusivity | duration | dependency | bargaining_power | revenue_path | proof_gate | risk
```

Key questions:

- Is the partner named by both sides, or only by the target company?
- Does the relationship include dollars, volumes, duration, exclusivity, milestones, or renewal terms?
- Is there proof of production deployment, purchase orders, usage, backlog, revenue conversion, or customer qualification?
- Who has bargaining power, and can the partner switch suppliers or build internally?
- Does the partnership validate product-market fit, solve distribution, relieve a supply bottleneck, or merely create PR?
- Does the relationship create concentration risk, margin pressure, working-capital needs, capex needs, or dilution risk?
- Are there hidden dependencies on one customer, supplier, exchange, cloud, government program, protocol, or geography?

Fluff filters:

- Treat MOUs, pilots, "collaborations," conference demos, and logo slides as `unresolved` until supported by primary evidence.
- If only one party announces the relationship, downgrade confidence unless corroborated.
- If no economics are visible, state what evidence would make it material.
- If the market is pricing a partnership as transformational, compare implied expectations with visible contractual evidence.

Output a partnership verdict: `validated`, `promising_unproven`, `commercial_but_small`, `strategic_dependency`, `marketing_fluff`, or `negative_signal`.

## Right-Security Test

For every thesis, compare the chosen security with alternatives:

- Is it the cleanest expression?
- Is exposure direct or second-order?
- Is the benefit already competed away?
- Could a supplier, customer, competitor, ETF, option, bond, commodity, or FX pair express the thesis better?
- What hidden risks come with this expression?

## Proof Gates

Convert narratives into observable gates:

- Filing, approval, customer qualification, production order, backlog, revenue conversion, margin change, financing, listing, index inclusion, unlock, policy decision, or technical milestone.
- State what happens if the gate is met, delayed, or missed.
- Mark watchlist ideas as watchlist ideas until gates are met.

Use a gate table:

```text
gate | source_to_check | expected_timing | evidence_required | scenario_impact | status | next_check_date
```

## Catalyst Map

Separate scheduled catalysts from unscheduled catalysts. For each catalyst, capture expected date or window, source, likely market interpretation, upside/downside asymmetry, and data needed afterward.

Grade catalyst quality:

- `hard`: filing deadline, earnings date, maturity, unlock, index rebalance, court date, policy meeting, scheduled protocol upgrade.
- `soft`: management target, expected customer decision, conference, product launch, macro release, industry data.
- `rumored`: social/news chatter, unattributed reports, speculative M&A, unconfirmed partner activity.
- `reflexive`: catalyst depends on price, flows, short squeeze, liquidity, or narrative attention.

For each catalyst, record:

```text
catalyst | type | date/window | source | affected thesis leg | market_expectation | upside_case | downside_case | evidence_after_event | confidence
```

Ask whether the catalyst changes intrinsic value, accelerates proof, changes liquidity/market structure, or only changes attention. Attention-only catalysts must not carry the thesis without evidence.

## Quant Profile

At minimum, compute total return, volatility, max drawdown, best/worst daily return, positive-day ratio, liquidity context, and benchmark correlation when data exists.

For deep work, add rolling returns, rolling volatility, regime splits, event windows, factor proxies, and peer comparisons when data is reliable.

## Market Structure

Use asset-specific mechanics:

- Equities: float, short interest, borrow, dilution, ATM/shelf capacity, insider/institutional ownership, lockups, index inclusion, liquidity.
- ETFs/funds: flows, creations/redemptions, premium/discount, concentration, rebalance.
- Crypto: circulating supply, unlocks, staking, exchange liquidity, treasury, governance concentration.
- Options: open interest, bid/ask, IV, expiry concentration, event risk.
- Bonds/rates: issue size, liquidity, callability, covenants, spread duration.

Market structure is an overlay. It should not become the thesis unless the situation is explicitly market-structure driven.

## Macro Sensitivity

Map sensitivity to rates, inflation, FX, commodities, credit spreads, liquidity, fiscal policy, regulation, geopolitics, and risk appetite.

State whether macro is a primary driver, secondary driver, or background risk.

## Valuation After Rerating

Separate thesis quality from setup quality:

- What scenario is the market already pricing?
- What revenue, margin, adoption, supply/demand, or macro outcome is implied?
- Is the asset validated but stretched, invalidated, under-researched, or still mispriced?
- What would make current valuation reasonable?

## Disagreement Ledger

Track credible disagreement:

- Which sources disagree?
- Is the disagreement factual, interpretive, timing-related, or valuation-related?
- What evidence would resolve it?
- What follow-up task should be added?

Disagreement is a diligence queue, not a nuisance.

## Monitoring Loop

Every dossier needs triggers:

- Scheduled: earnings, filings, macro releases, protocol upgrades, policy meetings, unlocks, index rebalances.
- Thresholds: price, valuation, drawdown, spread, liquidity, volume, correlation, supply, margin, revenue, TVL, hash rate, or other asset-specific metrics.
- Evidence: proof gates, invalidation signals, source conflicts, stale assumptions.
