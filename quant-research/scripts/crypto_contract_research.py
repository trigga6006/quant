#!/usr/bin/env python3
"""Crypto contract and protocol research helpers for the quant-research skill."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import statistics
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SHARED_RESEARCH_ROOT = Path("C:/Users/fowle/Documents/dev/OmniCapital/research")

ADDRESS_REGISTRY_COLUMNS = [
    "chain",
    "address",
    "address_type",
    "protocol",
    "canonical",
    "source_name",
    "source_url",
    "artifact_path",
    "confidence",
    "evidence",
    "caveats",
]

DEPLOYMENT_MATRIX_COLUMNS = [
    "chain",
    "address",
    "deployment_type",
    "canonical",
    "liquidity",
    "holder_concentration",
    "admin_risk",
    "bridge_risk",
    "confidence",
]

RISK_FLAG_COLUMNS = [
    "flag",
    "category",
    "severity",
    "evidence",
    "caveat",
    "downgrade_if",
    "upgrade_if",
]

CONFIDENCE_VALUES = {"confirmed", "high", "medium", "low", "unresolved"}
ADDRESS_TYPES = {
    "token",
    "contract",
    "proxy",
    "implementation",
    "governance",
    "treasury",
    "multisig",
    "deployer",
    "admin",
    "wallet",
    "pool",
    "bridge",
    "program",
    "mint",
    "vesting",
    "unknown",
}

EVM_PRIVILEGE_PATTERNS = {
    "upgrade": ["upgrade", "implementation", "proxyadmin"],
    "ownership": ["owner", "admin", "role", "grantrole", "revokerole", "transferownership"],
    "pause": ["pause", "unpause"],
    "mint": ["mint"],
    "burn": ["burn"],
    "blacklist": ["blacklist", "blocklist", "denylist", "whitelist"],
    "fees": ["fee", "tax", "settax", "setfee"],
    "limits": ["maxwallet", "maxtransaction", "limit", "cooldown"],
    "oracle": ["oracle", "pricefeed", "aggregator"],
    "bridge": ["bridge", "crosschain", "lzreceive", "endpoint"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_research_root() -> str:
    configured = os.environ.get("QUANT_RESEARCH_ROOT")
    if configured:
        return configured
    if DEFAULT_SHARED_RESEARCH_ROOT.exists():
        return str(DEFAULT_SHARED_RESEARCH_ROOT)
    return "research"


def safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "-" for ch in value.strip())
    return cleaned.strip("-") or "crypto-asset"


def init_crypto_dossier(asset: str, root: str | Path | None = None, depth: str = "standard") -> Path:
    now = utc_now()
    dossier = Path(root or default_research_root()) / safe_name(asset)
    crypto_root = dossier / "crypto"
    for directory in [
        "artifacts",
        "artifacts/evm",
        "artifacts/solana",
        "artifacts/audits",
        "artifacts/holders",
        "artifacts/events",
        "artifacts/transactions",
        "artifacts/fetches",
    ]:
        (crypto_root / directory).mkdir(parents=True, exist_ok=True)

    write_json_if_missing(
        crypto_root / "protocol-profile.json",
        {
            "asset": asset,
            "analysis_mode": "crypto_protocol",
            "depth": depth,
            "created_at": now,
            "last_updated": now,
            "chains": [],
            "canonical_sources": [],
            "identity_confidence": "unresolved",
        },
    )
    write_json_if_missing(
        crypto_root / "tokenomics.json",
        {
            "asset": asset,
            "classification": "unclear",
            "circulating_supply": "",
            "total_supply": "",
            "max_supply": "",
            "fdv": "",
            "emissions": [],
            "unlocks": [],
            "vesting": [],
            "treasury": [],
            "value_accrual": "",
            "caveats": [],
        },
    )
    write_json_if_missing(
        crypto_root / "security-review.json",
        {
            "asset": asset,
            "overall_risk": "unresolved",
            "not_formal_audit": True,
            "flags": [],
            "tooling": [],
            "caveats": [],
        },
    )
    write_json_if_missing(
        crypto_root / "onchain-forensics.json",
        {
            "asset": asset,
            "overall_risk": "unresolved",
            "entity_labels": [],
            "holder_summaries": [],
            "flow_summaries": [],
            "caveats": [],
        },
    )
    write_json_if_missing(
        crypto_root / "audit-summary.json",
        {
            "asset": asset,
            "audit_coverage": "unresolved",
            "highest_unresolved_severity": "unresolved",
            "deployed_code_matches_audit": "unverified",
            "audits": [],
            "major_caveats": [],
        },
    )

    write_csv_if_missing(crypto_root / "address-registry.csv", ADDRESS_REGISTRY_COLUMNS)
    write_csv_if_missing(crypto_root / "deployment-matrix.csv", DEPLOYMENT_MATRIX_COLUMNS)
    write_csv_if_missing(crypto_root / "risk-flags.csv", RISK_FLAG_COLUMNS)
    write_text_if_missing(crypto_root / "security-review.md", security_review_template(asset))
    write_text_if_missing(crypto_root / "onchain-forensics.md", onchain_forensics_template(asset))
    write_text_if_missing(crypto_root / "investment-diligence.md", investment_diligence_template(asset))
    return dossier


def write_json_if_missing(path: Path, payload: dict[str, Any]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text_if_missing(path: Path, text: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv_if_missing(path: Path, columns: list[str]) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(columns)


def security_review_template(asset: str) -> str:
    return (
        f"# {asset} Smart Contract / Security Review\n\n"
        "This is a research risk screen, not a formal audit.\n\n"
        "## Contract Identity\n\n"
        "## Verified Source and ABI\n\n"
        "## Upgradeability and Admin Powers\n\n"
        "## Token Controls\n\n"
        "## Oracle, Bridge, and Dependency Risk\n\n"
        "## Scam / Rug Screen\n\n"
        "## Audit Coverage\n\n"
        "## Findings and Caveats\n"
    )


def onchain_forensics_template(asset: str) -> str:
    return (
        f"# {asset} On-Chain Forensics\n\n"
        "## Address Resolution\n\n"
        "## Holder Concentration\n\n"
        "## Entity Labels\n\n"
        "## Liquidity and Pools\n\n"
        "## Deployer / Admin Behavior\n\n"
        "## Suspicious Activity\n\n"
        "## Caveats\n"
    )


def investment_diligence_template(asset: str) -> str:
    return (
        f"# {asset} Crypto Investment Diligence\n\n"
        "## Protocol Purpose and Market\n\n"
        "## Product and Usage\n\n"
        "## Tokenomics and Unlocks\n\n"
        "## TVL, Fees, Revenue, and Users\n\n"
        "## Governance\n\n"
        "## Cross-Chain Deployment Matrix\n\n"
        "## Valuation / Implied Expectations\n\n"
        "## Catalysts and Proof Gates\n\n"
        "## Risks and Diligence Queue\n"
    )


def validate_address_registry(path: str | Path) -> list[str]:
    registry = Path(path)
    if not registry.exists():
        return [f"address registry not found: {registry}"]
    errors: list[str] = []
    with registry.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        missing = [column for column in ADDRESS_REGISTRY_COLUMNS if column not in fieldnames]
        if missing:
            return [f"missing required columns: {', '.join(missing)}"]
        for line_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue
            address = (row.get("address") or "").strip()
            address_type = (row.get("address_type") or "").strip()
            confidence = (row.get("confidence") or "").strip()
            source_url = (row.get("source_url") or "").strip()
            artifact_path = (row.get("artifact_path") or "").strip()
            if not address:
                errors.append(f"line {line_number}: address is required")
            if address_type and address_type not in ADDRESS_TYPES:
                errors.append(f"line {line_number}: invalid address_type '{address_type}'")
            if confidence and confidence not in CONFIDENCE_VALUES:
                errors.append(f"line {line_number}: invalid confidence '{confidence}'")
            if not source_url and not artifact_path:
                errors.append(f"line {line_number}: source_url or artifact_path is required")
    return errors


def analyze_holders(path: str | Path, out: str | Path | None = None, top_n: int = 10) -> dict[str, Any]:
    holders = read_holders(path)
    total = sum(balance for _, balance in holders)
    if total <= 0:
        raise ValueError("holder balances must sum to a positive value")
    sorted_holders = sorted(holders, key=lambda item: item[1], reverse=True)
    shares = [balance / total for _, balance in sorted_holders]
    top_share = sum(shares[:top_n])
    hhi = sum(share * share for share in shares)
    summary = {
        "holder_file": str(path),
        "holder_count": len(holders),
        "total_balance": total,
        "top_n": top_n,
        "top_n_share": top_share,
        "top_1_share": shares[0],
        "hhi": hhi,
        "gini": gini([balance for _, balance in holders]),
        "concentration_risk": concentration_bucket(top_share, hhi),
        "top_holders": [
            {"address": address, "balance": balance, "share": balance / total}
            for address, balance in sorted_holders[:top_n]
        ],
    }
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def read_holders(path: str | Path) -> list[tuple[str, float]]:
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not {"address", "balance"}.issubset(set(reader.fieldnames or [])):
            raise ValueError("holder CSV must contain address and balance columns")
        holders = []
        for row in reader:
            address = (row.get("address") or "").strip()
            balance_raw = (row.get("balance") or "").replace(",", "").strip()
            if not address or not balance_raw:
                continue
            holders.append((address, float(balance_raw)))
    if not holders:
        raise ValueError("holder CSV contains no valid rows")
    return holders


def gini(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(value for value in values if value >= 0)
    total = sum(sorted_values)
    if total == 0:
        return 0.0
    weighted_sum = sum((index + 1) * value for index, value in enumerate(sorted_values))
    count = len(sorted_values)
    return (2 * weighted_sum) / (count * total) - (count + 1) / count


def concentration_bucket(top_share: float, hhi: float) -> str:
    if top_share >= 0.9 or hhi >= 0.75:
        return "critical"
    if top_share >= 0.6 or hhi >= 0.25:
        return "high"
    if top_share >= 0.35 or hhi >= 0.12:
        return "medium"
    return "low"


def analyze_evm_abi(path: str | Path, out: str | Path | None = None) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    abi = payload.get("abi", payload) if isinstance(payload, dict) else payload
    summary = analyze_evm_abi_data(abi)
    summary["abi_file"] = str(path)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def analyze_evm_abi_data(abi: list[dict[str, Any]]) -> dict[str, Any]:
    functions = [
        item.get("name", "")
        for item in abi
        if isinstance(item, dict) and item.get("type") == "function" and item.get("name")
    ]
    events = [
        item.get("name", "")
        for item in abi
        if isinstance(item, dict) and item.get("type") == "event" and item.get("name")
    ]
    categories: dict[str, list[str]] = {category: [] for category in EVM_PRIVILEGE_PATTERNS}
    privileged: list[str] = []
    for function in functions:
        lower = function.lower()
        for category, patterns in EVM_PRIVILEGE_PATTERNS.items():
            if any(pattern in lower for pattern in patterns):
                categories[category].append(function)
                if function not in privileged:
                    privileged.append(function)
    risk_bucket = evm_risk_bucket(categories)
    return {
        "function_count": len(functions),
        "event_count": len(events),
        "privileged_functions": privileged,
        "privilege_categories": {key: value for key, value in categories.items() if value},
        "risk_bucket": risk_bucket,
        "caveats": [
            "ABI pattern matching is a risk screen, not proof of exploitability.",
            "Review verified source, implementation contract, owner/admin addresses, and recent transactions.",
        ],
    }


def evm_risk_bucket(categories: dict[str, list[str]]) -> str:
    active = {category for category, functions in categories.items() if functions}
    if {"upgrade", "blacklist"}.issubset(active) or {"upgrade", "fees", "mint"}.issubset(active):
        return "critical"
    if "upgrade" in active or len(active) >= 3:
        return "high"
    if active:
        return "medium"
    return "low"


def analyze_solana_token(path: str | Path, out: str | Path | None = None) -> dict[str, Any]:
    metadata = json.loads(Path(path).read_text(encoding="utf-8"))
    summary = analyze_solana_token_data(metadata)
    summary["metadata_file"] = str(path)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def analyze_solana_token_data(metadata: dict[str, Any]) -> dict[str, Any]:
    mint_authority = first_present(metadata, ["mint_authority", "mintAuthority", "mint_authority_address"])
    freeze_authority = first_present(metadata, ["freeze_authority", "freezeAuthority", "freeze_authority_address"])
    risk_bucket = "low"
    if mint_authority and freeze_authority:
        risk_bucket = "high"
    elif mint_authority or freeze_authority:
        risk_bucket = "medium"
    return {
        "mint": first_present(metadata, ["mint", "address", "pubkey"]),
        "supply": first_present(metadata, ["supply", "totalSupply"]),
        "decimals": first_present(metadata, ["decimals"]),
        "mint_authority": mint_authority or "",
        "freeze_authority": freeze_authority or "",
        "mint_authority_status": "present" if mint_authority else "absent_or_not_supplied",
        "freeze_authority_status": "present" if freeze_authority else "absent_or_not_supplied",
        "risk_bucket": risk_bucket,
        "caveats": [
            "Authority absence can mean revoked or simply not supplied in the artifact.",
            "Confirm with explorer or Solana CLI before relying on this result.",
        ],
    }


def first_present(mapping: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return value
    return ""


def summarize_audit(path: str | Path, out: str | Path | None = None) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    lowered = text.lower()
    severities = ["critical", "high", "medium", "low", "informational"]
    counts = {severity: len(re.findall(rf"\b{severity}\b", lowered)) for severity in severities}
    unresolved_markers = ["unresolved", "not resolved", "acknowledged", "partially resolved"]
    summary = {
        "audit_file": str(path),
        "severity_mentions": counts,
        "contains_commit_hash": bool(re.search(r"\b[0-9a-f]{7,40}\b", lowered)),
        "mentions_out_of_scope": "out of scope" in lowered,
        "mentions_upgradeability": "upgrade" in lowered or "proxy" in lowered,
        "mentions_oracle": "oracle" in lowered,
        "mentions_bridge": "bridge" in lowered,
        "unresolved_markers": [marker for marker in unresolved_markers if marker in lowered],
        "caveats": [
            "Text summary is heuristic. The agent must read the audit report for scope, commit hash, and finding status.",
            "PDFs should be converted to text before using this command.",
        ],
    }
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def fetch_free_market_data(source: str, identifier: str, out_dir: str | Path) -> dict[str, Any]:
    endpoints = {
        "dexscreener-token": f"https://api.dexscreener.com/latest/dex/tokens/{identifier}",
        "defillama-protocol": f"https://api.llama.fi/protocol/{identifier}",
        "coingecko-simple": f"https://api.coingecko.com/api/v3/simple/price?ids={identifier}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true",
    }
    if source not in endpoints:
        raise ValueError(f"unknown free source '{source}'. Expected one of: {', '.join(sorted(endpoints))}")
    url = endpoints[source]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    result = {"source": source, "identifier": identifier, "url": url, "fetched_at": utc_now(), "ok": False}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "quant-research-skill/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
            result["status"] = getattr(response, "status", "")
            result["ok"] = True
    except (urllib.error.URLError, TimeoutError) as exc:
        result["error"] = str(exc)
        raw = json.dumps(result, indent=2)
    raw_path = out / f"{source}-{safe_name(identifier)}.json"
    raw_path.write_text(raw, encoding="utf-8")
    result["artifact_path"] = str(raw_path)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Crypto contract research helper utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-crypto-dossier", help="Create a protocol-level crypto dossier.")
    init_parser.add_argument("--asset", required=True)
    init_parser.add_argument("--root", default=default_research_root())
    init_parser.add_argument("--depth", default="standard", choices=["brief", "standard", "deep"])

    registry_parser = subparsers.add_parser("validate-address-registry", help="Validate crypto address registry CSV.")
    registry_parser.add_argument("--registry", required=True)

    holders_parser = subparsers.add_parser("analyze-holders", help="Analyze holder concentration from CSV.")
    holders_parser.add_argument("--holders", required=True)
    holders_parser.add_argument("--out", required=True)
    holders_parser.add_argument("--top-n", type=int, default=10)

    abi_parser = subparsers.add_parser("analyze-evm-abi", help="Flag privileged EVM ABI functions.")
    abi_parser.add_argument("--abi", required=True)
    abi_parser.add_argument("--out", required=True)

    solana_parser = subparsers.add_parser("analyze-solana-token", help="Analyze Solana token mint metadata JSON.")
    solana_parser.add_argument("--metadata", required=True)
    solana_parser.add_argument("--out", required=True)

    audit_parser = subparsers.add_parser("summarize-audit", help="Summarize converted audit text.")
    audit_parser.add_argument("--audit-text", required=True)
    audit_parser.add_argument("--out", required=True)

    fetch_parser = subparsers.add_parser("fetch-free-market-data", help="Fetch no-key public crypto market data.")
    fetch_parser.add_argument("--source", required=True, choices=["dexscreener-token", "defillama-protocol", "coingecko-simple"])
    fetch_parser.add_argument("--identifier", required=True)
    fetch_parser.add_argument("--out-dir", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init-crypto-dossier":
        print(init_crypto_dossier(args.asset, args.root, args.depth))
        return 0
    if args.command == "validate-address-registry":
        errors = validate_address_registry(args.registry)
        if errors:
            for error in errors:
                print(error)
            return 1
        print("address registry valid")
        return 0
    if args.command == "analyze-holders":
        print(json.dumps(analyze_holders(args.holders, args.out, args.top_n), indent=2))
        return 0
    if args.command == "analyze-evm-abi":
        print(json.dumps(analyze_evm_abi(args.abi, args.out), indent=2))
        return 0
    if args.command == "analyze-solana-token":
        print(json.dumps(analyze_solana_token(args.metadata, args.out), indent=2))
        return 0
    if args.command == "summarize-audit":
        print(json.dumps(summarize_audit(args.audit_text, args.out), indent=2))
        return 0
    if args.command == "fetch-free-market-data":
        print(json.dumps(fetch_free_market_data(args.source, args.identifier, args.out_dir), indent=2))
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
