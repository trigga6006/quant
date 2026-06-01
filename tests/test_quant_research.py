import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "quant-research" / "scripts" / "quant_research.py"
SPEC = importlib.util.spec_from_file_location("quant_research", SCRIPT_PATH)
quant_research = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["quant_research"] = quant_research
SPEC.loader.exec_module(quant_research)


class QuantResearchTests(unittest.TestCase):
    def test_skill_contains_partnership_bottleneck_and_catalyst_frameworks(self):
        root = SCRIPT_PATH.parents[1]
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        lenses = (root / "references" / "research-lenses.md").read_text(encoding="utf-8")
        output_templates = (root / "references" / "output-templates.md").read_text(encoding="utf-8")
        crypto_routing = (root / "references" / "crypto-smart-routing.md").read_text(encoding="utf-8")
        crypto_playbook = (root / "references" / "crypto-contract-playbook.md").read_text(encoding="utf-8")

        self.assertIn("Strategic partnerships, ecosystem dependencies", skill)
        self.assertIn("Strategic Partnerships and Ecosystem Map", lenses)
        self.assertIn("relationship_type", lenses)
        self.assertIn("constraint | owner/controller", lenses)
        self.assertIn("catalyst | type | date/window", lenses)
        self.assertIn("Partnerships and Ecosystem Dependencies", output_templates)
        self.assertIn("Crypto Smart Routing", crypto_routing)
        self.assertIn("Scam/rug", crypto_playbook)
        self.assertIn("Cross-Chain Deployment Matrix", crypto_playbook)
        self.assertIn("Smart Contract / Security Review", output_templates)

    def test_init_dossier_creates_required_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            dossier = quant_research.init_dossier("TEST", "equity", temp)

            for directory in ["source-notes", "data", "charts", "quant", "valuation", "reports"]:
                self.assertTrue((dossier / directory).is_dir())

            for filename in [
                "asset-profile.json",
                "analysis-manifest.json",
                "evidence-ledger.csv",
                "source-registry.json",
                "assumptions.md",
                "limitations.md",
                "watchlist-triggers.yaml",
            ]:
                self.assertTrue((dossier / filename).exists())

            profile = json.loads((dossier / "asset-profile.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["asset"], "TEST")
            self.assertEqual(profile["asset_type"], "equity")

    def test_validate_ledger_accepts_valid_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "ledger.csv"
            self.write_ledger(
                ledger,
                [
                    {
                        "claim_id": "T-001",
                        "claim": "Test claim",
                        "asset": "TEST",
                        "source_type": "computed",
                        "source_name": "unit test",
                        "source_url": "",
                        "source_date": "2026-05-29",
                        "access_date": "2026-05-29",
                        "evidence_excerpt": "calculated locally",
                        "artifact_path": "quant/summary.json",
                        "confidence": "high",
                        "caveats": "",
                        "corroboration_status": "single_source",
                    }
                ],
            )

            self.assertEqual(quant_research.validate_ledger(ledger), [])

    def test_validate_ledger_rejects_bad_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "ledger.csv"
            self.write_ledger(
                ledger,
                [
                    {
                        "claim_id": "T-001",
                        "claim": "",
                        "asset": "TEST",
                        "source_type": "rumor",
                        "source_name": "unit test",
                        "source_url": "",
                        "source_date": "2026-05-29",
                        "access_date": "2026-05-29",
                        "evidence_excerpt": "",
                        "artifact_path": "",
                        "confidence": "certain",
                        "caveats": "",
                        "corroboration_status": "single_source",
                    }
                ],
            )

            errors = quant_research.validate_ledger(ledger)
            self.assertIn("line 2: claim is required", errors)
            self.assertIn("line 2: invalid source_type 'rumor'", errors)
            self.assertIn("line 2: invalid confidence 'certain'", errors)
            self.assertIn("line 2: source_url or artifact_path is required", errors)

    def test_analyze_prices_writes_summary_and_returns(self):
        with tempfile.TemporaryDirectory() as temp:
            prices = Path(temp) / "prices.csv"
            prices.write_text(
                "date,close\n"
                "2026-01-01,100\n"
                "2026-01-02,110\n"
                "2026-01-03,105\n"
                "2026-01-04,120\n"
                "2026-01-05,90\n",
                encoding="utf-8",
            )
            out = Path(temp) / "out"

            summary = quant_research.analyze_prices(prices, out)

            self.assertAlmostEqual(summary["total_return"], -0.10)
            self.assertAlmostEqual(summary["max_drawdown"], -0.25)
            self.assertEqual(summary["observations"], 5)
            self.assertTrue((out / "quant-summary.json").exists())
            self.assertTrue((out / "returns.csv").exists())

            with (out / "returns.csv").open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 4)

    @staticmethod
    def write_ledger(path, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=quant_research.LEDGER_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
