# Crypto Contract Playbook

Use this reference for crypto tokens, protocols, contracts, wallets, mints, programs, DAOs, DEX pools, bridges, and yield products. This workflow is a risk screen and research framework, not a formal audit.

## Dossier Structure

Run:

```bash
python quant-research/scripts/crypto_contract_research.py init-crypto-dossier --asset <ASSET>
```

Protocol-level dossier:

```text
research/<ASSET>/crypto/
  protocol-profile.json
  address-registry.csv
  deployment-matrix.csv
  tokenomics.json
  security-review.md
  security-review.json
  onchain-forensics.md
  onchain-forensics.json
  investment-diligence.md
  risk-flags.csv
  audit-summary.json
  artifacts/
    evm/
    solana/
    audits/
    holders/
    events/
    transactions/
    fetches/
```

## Modules

Investment diligence:

- Protocol purpose, market/category, competitors, users, TVL, volume, fees, revenue, retention, developer activity, governance, treasury, catalysts, valuation, and implied expectations.
- Token value accrual: fees, buybacks, burns, staking, governance, revenue share, utility, collateral, or no clear accrual.
- Sustainability: distinguish real usage from incentive farming.

Tokenomics:

- Circulating supply, total/max supply, FDV, market cap, float, emissions, unlocks, vesting, team/investor allocation, treasury, liquidity mining, staking yield source, inflation, supply sinks, bridge/wrapped supply, rebasing/elastic mechanics, mint authority, and sell-pressure calendar.
- Classify tokenomics as `sustainable`, `incentive-dependent`, `reflexive`, `extractive`, `unclear`, or `high-risk`.

Smart-contract/security review:

- Verified source and ABI availability.
- Proxy/upgradeability and implementation address.
- Owner/admin roles, multisig, timelock, governance coverage.
- Mint, burn, pause, blacklist/whitelist, tax/fee, max-wallet, max-transaction, cooldown, rescue-token, oracle, and bridge controls.
- Dependency risk: oracle, bridge, external protocol, privileged keeper, sequencer, cross-chain messenger.
- Known audits, exploit history, bug bounty, recent upgrades, and unresolved findings.

On-chain forensics:

- Deployer/admin wallet behavior, holder concentration, top wallet flows, LP/pool liquidity, CEX/DEX flows where free data allows, emissions/unlocks, suspicious transfers, privileged calls, event logs, and real usage vs farming.
- Wallet labels must be evidence-bucketed: `confirmed`, `strong_inference`, `weak_inference`, or `unknown`.

Scam/rug risk screen:

- Unverified source, EOA owner, active mint/freeze/blacklist/tax controls, upgradeable proxy, hidden limits, fake renounce, clone contract, no LP lock/burn evidence, shallow liquidity, top-holder concentration, suspicious deployer transfers, buy/sell asymmetry, recent privileged calls, or unsupported cross-chain deployments.

## EVM Workflow

1. Resolve chain, token contract, proxy, implementation, governance, treasury/multisig, deployer, major pools, bridge contracts, and staking contracts.
2. Save ABI/source/explorer exports under `crypto/artifacts/evm/`.
3. Run:

```bash
python quant-research/scripts/crypto_contract_research.py analyze-evm-abi --abi <abi.json> --out <summary.json>
```

4. Use optional tools if installed: Slither, Mythril, Foundry/cast. If unavailable, record the skipped tool and use ABI/source/manual checklist.
5. Validate address provenance:

```bash
python quant-research/scripts/crypto_contract_research.py validate-address-registry --registry <address-registry.csv>
```

## Solana Workflow

1. Resolve token mint, program ID, upgrade authority, IDL if Anchor, governance, treasury, pools, and major token accounts.
2. Save explorer/CLI exports under `crypto/artifacts/solana/`.
3. Run:

```bash
python quant-research/scripts/crypto_contract_research.py analyze-solana-token --metadata <mint.json> --out <summary.json>
```

4. Check mint authority, freeze authority, supply/decimals, holder concentration, program upgrade authority, IDL availability, and multisig/governance controls.
5. Use Solana CLI and Anchor if installed. If unavailable, record the gap and use explorer/exported artifacts.

## Cross-Chain Deployment Matrix

Analyze all major deployments for a token/protocol. Fill:

```text
chain | address | deployment_type | canonical | liquidity | holder_concentration | admin_risk | bridge_risk | confidence
```

Flag:

- Weaker admin controls on one chain.
- Bridge custody assumptions.
- Fragmented or fake liquidity.
- Clone/fake contracts.
- Unsupported deployments.
- Governance coverage gaps.

## Holder Analysis

For exported holder CSVs with `address,balance`, run:

```bash
python quant-research/scripts/crypto_contract_research.py analyze-holders --holders holders.csv --out holder-analysis.json
```

Use the output for top-holder share, HHI, rough Gini, and qualitative concentration risk. Treat labels as unverified unless separately evidenced.

## Audit Ingestion

Read audit PDFs/reports and extract:

- audit firm, date, audited version/commit hash, in-scope contracts, out-of-scope contracts, deployed addresses, findings by severity, unresolved findings, centralization warnings, oracle/bridge/dependency warnings, economic warnings, and whether deployed contracts match audited versions.

If a PDF is converted to text, run:

```bash
python quant-research/scripts/crypto_contract_research.py summarize-audit --audit-text audit.txt --out audit-summary.json
```

Do not say "audited" without scope and freshness. Upgradeable contracts need deployed implementation matching.

## Free Data Fetching

Reliable baseline is saved/exported artifacts. Optional no-key fetchers may be used:

```bash
python quant-research/scripts/crypto_contract_research.py fetch-free-market-data --source dexscreener-token --identifier <token-address> --out-dir crypto/artifacts/fetches
python quant-research/scripts/crypto_contract_research.py fetch-free-market-data --source defillama-protocol --identifier <protocol-slug> --out-dir crypto/artifacts/fetches
python quant-research/scripts/crypto_contract_research.py fetch-free-market-data --source coingecko-simple --identifier <coingecko-id> --out-dir crypto/artifacts/fetches
```

If blocked or rate-limited, record the failure and continue with browser/exported data.

## Risk Buckets

Use qualitative buckets only: `low`, `medium`, `high`, `critical`, or `unresolved`. Every bucket needs evidence, caveat, and conditions that would raise or lower the risk. Never state that a contract is safe.
