# Asset-Class Playbooks

Start every run by identifying the instrument. Apply the matching section and document any unavailable data.

## Equities and ADRs

Required checks:

- Business model, segments, geography, customers, suppliers, and competitive position.
- Strategic partnerships, named customers, suppliers, distribution channels, ecosystem dependencies, and concentration risk.
- Filings, earnings releases, investor decks, insider/institutional ownership when free.
- Revenue, margins, cash flow, balance sheet, dilution risk, capital allocation, and guidance.
- Price history, volatility, drawdown, liquidity, beta/correlation, and event windows.
- Valuation: multiples, historical ranges, peer comparison, implied expectations, and DCF only when assumptions are supportable.
- Proof gates: earnings beats/misses, guidance changes, customer wins, partner validation, regulatory approvals, capacity additions, margin inflection, financing events.
- Demand-alpha checks when relevant: separate narrative from observed demand, map demand into revenue/margin/cash-flow/balance-sheet lines, rank small pure beneficiaries, test market misclassification, and build a 1-4 quarter validation chain.

Common gaps: transcripts may be paywalled, segment details may be limited, peer data may be inconsistent, short interest may lag.

Partnership checks: inspect both sides of any named relationship, distinguish signed commercial terms from pilots or marketing language, and look for revenue conversion, backlog, qualification, exclusivity, prepayments, or concentration risk.

## ETFs and Funds

Required checks:

- Sponsor, index/methodology, holdings, expense ratio, liquidity, distributions, tracking behavior, and concentration.
- NAV or premium/discount for closed-end funds or products where relevant.
- Quant profile against the benchmark or relevant exposure proxy.
- Flow and rebalance mechanics when free data exists.

Valuation focuses on underlying exposure and structure rather than issuer earnings.

## Crypto Assets

Required checks:

- Protocol purpose, token utility, supply schedule, unlocks, governance, security model, developer activity, liquidity, exchange support, and on-chain activity when free.
- Ecosystem partners: exchanges, custodians, bridges, wallets, validators, developers, grants, market makers, foundations, and major integrations.
- Smart routing: determine whether the user supplied a token symbol, protocol name, EVM contract address, Solana mint/program, wallet, transaction, pool, or bridge.
- Contract/security review: verified source, ABI/IDL, proxy/upgradeability, admin powers, mint/freeze/pause/blacklist/fee controls, oracle/bridge/dependency risk, audit coverage, exploit history, and scam/rug risk screen.
- On-chain forensics: holder concentration, deployer/admin behavior, treasury/multisig, whale flows, liquidity pools, suspicious transfers, privileged calls, and wallet/entity labels with confidence levels.
- Cross-chain deployment matrix for all major deployments, including canonical/native, wrapped/bridged, L2, pool, staking, governance, and treasury addresses.
- Quant profile using spot prices, volatility, drawdowns, correlations, and regime behavior.
- Market structure: circulating supply, unlocks, staking, exchange reserves, liquidity, and protocol revenues where available.

Valuation uses implied adoption, fees, flows, supply/demand, comparable protocols, and scenario analysis. Do not force equity-style multiples unless the metric is meaningful.

Partnership checks: separate real integrations and usage from ecosystem announcements, grants, or exchange-listing hype. Confirm with protocol docs, repositories, governance posts, public dashboards, and the partner's own announcement when possible.

Tokenomics checks: circulating/total/max supply, FDV, float, emissions, vesting, unlocks, team/investor allocation, treasury, incentives, staking yield source, value accrual, inflation, supply sinks, bridge/wrapped supply, mint authority, and sell-pressure calendar.

## Commodities

Required checks:

- Supply/demand balance, inventories, production capacity, seasonality, transportation/storage, policy, geopolitics, and futures curve shape where available.
- Quant profile using spot or futures proxies.
- Sensitivity to rates, FX, inflation, growth, and policy.

Valuation focuses on marginal cost, inventory cycle, curve structure, and scenario ranges.

## FX

Required checks:

- Interest-rate differentials, inflation, current account, fiscal position, central-bank reaction function, liquidity, positioning, and geopolitical risk.
- Quant profile, carry, volatility, drawdowns, and correlation with risk assets.

Valuation uses real effective exchange rates, purchasing-power parity as a rough anchor, rate differentials, and macro scenarios.

## Rates and Bonds

Required checks:

- Issuer, maturity, coupon, yield, duration, convexity, credit quality, seniority, covenants, liquidity, callability, and inflation linkage where applicable.
- Macro sensitivity to policy rates, inflation, curve shape, and credit spreads.

Valuation uses yield, spread, duration, credit/inflation/rate sensitivity, and scenario analysis.

## Options

Required checks:

- Underlying thesis, expiration, strike, payoff, breakeven, liquidity, bid/ask, implied volatility, and event calendar.
- Greeks only if reliable free chain data is available.

Options analysis must distinguish directional thesis from volatility thesis. If chain data is unreliable, analyze payoff and risks without pretending precision.

## Situations, Themes, and Catalysts

Required checks:

- Define the situation, affected securities, timeline, decision points, and source of market mispricing.
- Identify the cleanest expression and alternatives.
- Map proof gates, invalidation signals, catalysts, partnership/ecosystem dependencies, bottlenecks, and watchlist triggers.
- Translate the theme into financial-statement transmission and alpha elasticity before naming winners.
- Use source disagreement as a diligence queue.
