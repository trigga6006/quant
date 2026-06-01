# Crypto Smart Routing

Use this router to infer whether the crypto desk should activate. Do not require the user to write exact commands.

## Activate Crypto Workflow

Activate crypto analysis when the prompt, asset, or discovered sources include:

- Contract-like identifiers: EVM `0x...` address, Solana base58 mint/program/account, transaction hash, wallet address.
- Crypto language: coin, token, protocol, DAO, DEX, AMM, pool, LP, bridge, staking, yield, airdrop, TVL, fees, revenue, emissions, unlocks, governance, treasury, multisig, mint, contract, wallet, deployer.
- Known crypto assets or protocols discovered through search: CoinGecko, DefiLlama, DEXScreener, GeckoTerminal, official docs, explorer pages, GitHub, governance forums.
- User intent: "is this safe", "rug", "honeypot", "contract", "wallet flows", "tokenomics", "on-chain", "audit", "exploit", "liquidity", "holders".

Do not activate smart-contract analysis for ordinary public equities, ETFs, bonds, commodities, FX, rates, or macro topics unless the thesis explicitly involves tokenized assets, protocol exposure, or blockchain contracts.

## Depth Inference

- Brief/light: "quick", "brief", "light pass", "sanity check", "is this obviously sketchy".
- Standard: "research", "look into", "diligence", "analyze", "is this investable".
- Deep/aggressive: "deep", "full dive", "aggressive", "audit", "forensic", "exploit", "wallet flows", "rug", "scam", "contract risk", "trace".

If the prompt is vague but crypto signals are strong, choose `standard`. If the user asks for safety, exploitability, scam/rug risk, or wallet flows, bias toward security/on-chain modules.

## Identity Resolution Gate

Before contract-level analysis, resolve:

```text
asset/protocol | symbol | chain | canonical website/docs | token contract/mint | program ID | governance | treasury/multisig | major pools | source confidence
```

Use official docs, explorer pages, CoinGecko, DefiLlama, DEXScreener/GeckoTerminal, GitHub, governance forums, and project announcements. Require at least two corroborating sources for major addresses when possible. If only one weak source exists, mark confidence `unresolved`.

Warn when:

- The symbol is shared by multiple assets.
- The token exists on many chains.
- The address might be a wrapped/bridged token, LP token, pool, proxy, or implementation.
- Search results show copycat or fake contracts.

Record address provenance in `crypto/address-registry.csv`.

## Routing Examples

- "research JPM deep" -> equity workflow only.
- "research AERO deep" -> resolve whether AERO is Aerodrome/protocol; if yes, crypto workflow.
- "analyze 0xabc..." -> EVM contract workflow immediately.
- "look into this Solana mint" -> Solana token/program workflow.
- "is this token a rug" -> brief or deep crypto risk screen depending on user wording.
