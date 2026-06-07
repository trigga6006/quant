# Source Playbook

Use free sources first. Prefer sources that are direct, dated, downloadable, and stable.

## Fallback Ladder

1. Primary, regulatory, issuer, exchange, central bank, fund sponsor, or protocol sources.
2. Filings, investor relations material, earnings releases, transcripts, whitepapers, and fact sheets.
3. Free market-data APIs or downloadable datasets.
4. Reputable free financial portals.
5. News, search results, blogs, newsletters, social posts, and analyst commentary.
6. User-provided files or notes.
7. Mark unavailable data as a gap and reduce confidence.

## Common Free Sources

Equities and ADRs:

- SEC EDGAR filings and company investor relations pages.
- Earnings releases, investor decks, annual reports, proxy statements, and 8-Ks.
- Customer, supplier, and partnership evidence from both counterparties: press releases, filings, procurement portals, partner directories, app/cloud marketplaces, case studies, standards bodies, and conference presentations.
- Exchange pages for listing, trading, and corporate-action context.
- Free market-data sources such as Yahoo Finance, Stooq, Nasdaq pages, or Alpha Vantage free tier if the user supplies a key.

ETFs and funds:

- Sponsor pages, prospectuses, fact sheets, holdings files, NAV data, expense ratios, and distribution histories.
- Index methodology pages when a fund tracks an index.

Macro, rates, and credit:

- FRED, Treasury, Federal Reserve, ECB, BOE, BOJ, BLS, BEA, Census, IMF, World Bank, and national statistical agencies.
- Official yield curves, policy statements, inflation releases, and credit-spread datasets when free.

Crypto and protocols:

- Protocol documentation, official explorers, GitHub repositories, governance forums, tokenomics pages, and foundation/project disclosures.
- Partner and ecosystem evidence from exchanges, custodians, wallets, bridges, foundation grant pages, governance proposals, public dashboards, developer repositories, and integration docs.
- CoinGecko, CoinMarketCap, DefiLlama, Dune public dashboards, and exchange data as leads or market-data sources.
- EVM: Etherscan-family explorer pages, verified source, ABI, proxy/implementation pages, contract events, token holders, DEXScreener, GeckoTerminal, DefiLlama, CoinGecko, official docs, audit reports, and exploit writeups.
- Solana: Solscan, SolanaFM, Solana Explorer, SPL mint metadata, program upgrade authority, Anchor IDL when available, token holder exports, governance pages, pool pages, audit reports, and exploit writeups.

Commodities and FX:

- Central banks, government statistical agencies, EIA, USDA, OPEC, exchange pages, futures contract specifications, and free macro datasets.

Options and market structure:

- Official option chain pages, OCC resources, exchange pages, SEC filings for dilution, company shelf/ATM filings, short-interest pages, fund flow pages, and public ownership data.

Capital structure and float dynamics:

- SEC S-1, S-3, F-3, 424B, 10-K, 10-Q, 8-K, 20-F, 6-K, prospectus supplements, ATM sales agreements, equity distribution agreements, resale registration statements, PIPE agreements, warrant agreements, convertible indentures, credit agreements, covenant summaries, lockup agreements, beneficial ownership tables, transfer-agent share counts, short-interest reports, borrow data where free, and investor presentations.

Secondary research:

- Use news, X, Substack, blogs, podcasts, and analyst notes to find leads, disagreements, and questions. Treat them as `secondary` unless corroborated by stronger evidence.

## Partnership and Catalyst Source Rules

For material partnerships, try to find evidence from both parties. If the target company announces a deal and the counterparty is silent, record that silence as a caveat.

Prefer signed-contract evidence, filings, procurement records, revenue disclosures, backlog, usage metrics, qualification milestones, standards documents, or partner directories over press-release language.

For catalysts, prefer dated primary sources: earnings calendars, SEC filing deadlines, court dockets, policy meeting calendars, unlock schedules, index methodology/rebalance calendars, protocol governance timelines, and company event pages.

## Demand Alpha Source Rules

For news-to-alpha work, prioritize evidence that proves demand has already changed: filings, earnings-call commentary, backlog/order commentary, procurement portals, customer deployments, supplier lead times, pricing changes, channel checks, app/user metrics, production schedules, import/export data, and customer/supplier corroboration.

Do not treat a viral story, executive quote, conference demo, or product announcement as alpha until the research identifies who gets paid, which financial line changes, and when public filings or calls can verify it.

## Crypto Free-Source Rules

Use free sources and exported artifacts first. API keys are optional only if the user provides them. Do not require paid endpoints for a crypto run.

Prefer official docs, verified explorer pages, protocol repositories, governance forums, audit PDFs, DefiLlama, CoinGecko, DEXScreener, GeckoTerminal, and public dashboards. Record endpoint URLs, access time, raw artifact path, and caveats for every fetch or export.

Never trust a contract address from a single search result. Corroborate with official docs, explorer labels, CoinGecko/DefiLlama, governance docs, or the project's own UI before treating it as canonical.

## Source Selection Rules

Record publication dates and access dates. Prefer downloadable CSV, JSON, PDF, or HTML tables over screenshots. Keep exact URLs in the ledger.

If two sources conflict, add both to the evidence ledger and create a disagreement item rather than choosing silently.
