#!/usr/bin/env python3
"""Helper utilities for the quant-research skill."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


LEDGER_COLUMNS = [
    "claim_id",
    "claim",
    "asset",
    "source_type",
    "source_name",
    "source_url",
    "source_date",
    "access_date",
    "evidence_excerpt",
    "artifact_path",
    "confidence",
    "caveats",
    "corroboration_status",
]

SOURCE_TYPES = {
    "primary",
    "regulatory",
    "issuer",
    "exchange",
    "market_data",
    "computed",
    "secondary",
    "user_provided",
}

CONFIDENCE_VALUES = {"high", "medium", "low", "unresolved"}

CORROBORATION_VALUES = {
    "",
    "single_source",
    "corroborated",
    "conflicting",
    "unresolved",
}

DEFAULT_SHARED_RESEARCH_ROOT = Path("C:/Users/fowle/Documents/dev/OmniCapital/research")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def safe_asset_name(asset: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "-" for ch in asset.strip())
    return cleaned.strip("-") or "asset"


def default_research_root() -> str:
    configured = os.environ.get("QUANT_RESEARCH_ROOT")
    if configured:
        return configured
    if DEFAULT_SHARED_RESEARCH_ROOT.exists():
        return str(DEFAULT_SHARED_RESEARCH_ROOT)
    return "research"


def init_dossier(asset: str, asset_type: str, root: str | Path = "research", depth: str = "standard") -> Path:
    now = utc_now()
    dossier = Path(root) / safe_asset_name(asset)
    for child in ["source-notes", "data", "charts", "quant", "valuation", "reports"]:
        (dossier / child).mkdir(parents=True, exist_ok=True)

    asset_profile = {
        "asset": asset,
        "asset_type": asset_type,
        "canonical_name": "",
        "identifiers": {},
        "venue": "",
        "currency": "",
        "benchmark": "",
        "created_at": now,
        "last_updated": now,
    }
    write_json_if_missing(dossier / "asset-profile.json", asset_profile)

    manifest = {
        "asset": asset,
        "depth": depth,
        "mode": "initial",
        "created_at": now,
        "last_updated": now,
        "reports": [],
        "data_artifacts": [],
        "quant_artifacts": [],
        "valuation_artifacts": [],
        "known_gaps": [],
    }
    write_json_if_missing(dossier / "analysis-manifest.json", manifest)
    write_json_if_missing(dossier / "source-registry.json", {"asset": asset, "sources": []})

    ledger_path = dossier / "evidence-ledger.csv"
    if not ledger_path.exists():
        with ledger_path.open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerow(LEDGER_COLUMNS)

    write_text_if_missing(
        dossier / "assumptions.md",
        "# Assumptions\n\nRecord explicit assumptions used in scenarios, valuation, and computed work.\n",
    )
    write_text_if_missing(
        dossier / "limitations.md",
        "# Limitations\n\nRecord missing, stale, blocked, inconsistent, or low-confidence data.\n",
    )
    write_text_if_missing(
        dossier / "watchlist-triggers.yaml",
        "scheduled: []\nthresholds: []\nproof_gates: []\ninvalidation_signals: []\n",
    )

    report = dossier / "reports" / f"{datetime.now().date().isoformat()}-initial-report.md"
    write_text_if_missing(
        report,
        f"# {asset} Initial Research Report\n\n"
        "## Executive Summary\n\n"
        "## Evidence Quality and Data Gaps\n\n"
        "## Quantitative Profile\n\n"
        "## Scenarios\n\n"
        "## Proof Gates and Invalidation Signals\n\n"
        "## Monitoring Plan\n",
    )
    return dossier


def write_json_if_missing(path: Path, payload: dict) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text_if_missing(path: Path, text: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def validate_ledger(path: str | Path) -> list[str]:
    ledger = Path(path)
    if not ledger.exists():
        return [f"ledger not found: {ledger}"]

    errors: list[str] = []
    with ledger.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        missing = [column for column in LEDGER_COLUMNS if column not in fieldnames]
        if missing:
            return [f"missing required columns: {', '.join(missing)}"]

        for line_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue
            claim = (row.get("claim") or "").strip()
            source_type = (row.get("source_type") or "").strip()
            confidence = (row.get("confidence") or "").strip()
            corroboration = (row.get("corroboration_status") or "").strip()
            source_url = (row.get("source_url") or "").strip()
            artifact_path = (row.get("artifact_path") or "").strip()

            if not claim:
                errors.append(f"line {line_number}: claim is required")
            if source_type not in SOURCE_TYPES:
                errors.append(f"line {line_number}: invalid source_type '{source_type}'")
            if confidence not in CONFIDENCE_VALUES:
                errors.append(f"line {line_number}: invalid confidence '{confidence}'")
            if corroboration not in CORROBORATION_VALUES:
                errors.append(f"line {line_number}: invalid corroboration_status '{corroboration}'")
            if not source_url and not artifact_path:
                errors.append(f"line {line_number}: source_url or artifact_path is required")
    return errors


@dataclass
class PricePoint:
    date: str
    close: float


def read_prices(path: str | Path) -> list[PricePoint]:
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"date", "close"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("price CSV must contain date and close columns")
        points = [
            PricePoint(row["date"], float(row["close"]))
            for row in reader
            if row.get("date") and row.get("close")
        ]
    points.sort(key=lambda item: item.date)
    if len(points) < 2:
        raise ValueError("price CSV must contain at least two valid rows")
    return points


def daily_returns(points: list[PricePoint]) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for previous, current in zip(points, points[1:]):
        if previous.close <= 0:
            raise ValueError("close prices must be positive")
        rows.append({"date": current.date, "return": (current.close / previous.close) - 1.0})
    return rows


def max_drawdown(points: list[PricePoint]) -> float:
    peak = points[0].close
    worst = 0.0
    for point in points:
        peak = max(peak, point.close)
        drawdown = (point.close / peak) - 1.0
        worst = min(worst, drawdown)
    return worst


def analyze_prices(prices: str | Path, out_dir: str | Path, benchmark: str | Path | None = None) -> dict:
    points = read_prices(prices)
    returns = daily_returns(points)
    return_values = [float(row["return"]) for row in returns]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    total_return = (points[-1].close / points[0].close) - 1.0
    volatility = statistics.stdev(return_values) * math.sqrt(252) if len(return_values) > 1 else 0.0
    positive_day_ratio = sum(1 for value in return_values if value > 0) / len(return_values)

    summary = {
        "price_file": str(prices),
        "benchmark_file": str(benchmark) if benchmark else "",
        "start_date": points[0].date,
        "end_date": points[-1].date,
        "observations": len(points),
        "return_observations": len(returns),
        "start_close": points[0].close,
        "end_close": points[-1].close,
        "total_return": total_return,
        "annualized_volatility": volatility,
        "max_drawdown": max_drawdown(points),
        "best_daily_return": max(return_values),
        "worst_daily_return": min(return_values),
        "positive_day_ratio": positive_day_ratio,
        "charting": {"available": False, "reason": "matplotlib not attempted"},
    }

    benchmark_points = read_prices(benchmark) if benchmark else []
    if benchmark_points:
        benchmark_returns = [float(row["return"]) for row in daily_returns(benchmark_points)]
        paired = list(zip(return_values, benchmark_returns))
        if len(paired) > 1:
            asset_values = [item[0] for item in paired]
            bench_values = [item[1] for item in paired]
            summary["benchmark_correlation"] = correlation(asset_values, bench_values)

    write_returns(out / "returns.csv", returns)
    maybe_write_charts(points, out, summary)
    (out / "quant-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def correlation(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("correlation requires equal-length series with at least two observations")
    left_mean = statistics.mean(left)
    right_mean = statistics.mean(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_var = sum((a - left_mean) ** 2 for a in left)
    right_var = sum((b - right_mean) ** 2 for b in right)
    denominator = math.sqrt(left_var * right_var)
    return numerator / denominator if denominator else 0.0


def write_returns(path: Path, rows: Iterable[dict[str, float | str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "return"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def maybe_write_charts(points: list[PricePoint], out: Path, summary: dict) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on local optional package
        summary["charting"] = {"available": False, "reason": f"matplotlib unavailable: {exc}"}
        return

    dates = [point.date for point in points]
    closes = [point.close for point in points]
    peaks: list[float] = []
    peak = closes[0]
    drawdowns: list[float] = []
    for close in closes:
        peak = max(peak, close)
        peaks.append(peak)
        drawdowns.append((close / peak) - 1.0)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes)
    plt.xticks(rotation=45, ha="right")
    plt.title("Close Price")
    plt.tight_layout()
    plt.savefig(out / "price-chart.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, drawdowns)
    plt.xticks(rotation=45, ha="right")
    plt.title("Drawdown")
    plt.tight_layout()
    plt.savefig(out / "drawdown-chart.png")
    plt.close()

    summary["charting"] = {
        "available": True,
        "price_chart": str(out / "price-chart.png"),
        "drawdown_chart": str(out / "drawdown-chart.png"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Quant research skill helper utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-dossier", help="Create a research dossier tree.")
    init_parser.add_argument("--asset", required=True)
    init_parser.add_argument("--asset-type", required=True)
    init_parser.add_argument("--root", default=default_research_root())
    init_parser.add_argument("--depth", default="standard", choices=["brief", "standard", "deep"])

    ledger_parser = subparsers.add_parser("validate-ledger", help="Validate an evidence ledger CSV.")
    ledger_parser.add_argument("--ledger", required=True)

    prices_parser = subparsers.add_parser("analyze-prices", help="Analyze a local date/close price CSV.")
    prices_parser.add_argument("--prices", required=True)
    prices_parser.add_argument("--out-dir", required=True)
    prices_parser.add_argument("--benchmark")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init-dossier":
        dossier = init_dossier(args.asset, args.asset_type, args.root, args.depth)
        print(dossier)
        return 0

    if args.command == "validate-ledger":
        errors = validate_ledger(args.ledger)
        if errors:
            for error in errors:
                print(error)
            return 1
        print("ledger valid")
        return 0

    if args.command == "analyze-prices":
        summary = analyze_prices(args.prices, args.out_dir, args.benchmark)
        print(json.dumps(summary, indent=2))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
