import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "quant-research" / "scripts" / "crypto_contract_research.py"
SPEC = importlib.util.spec_from_file_location("crypto_contract_research", SCRIPT_PATH)
crypto_contract_research = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["crypto_contract_research"] = crypto_contract_research
SPEC.loader.exec_module(crypto_contract_research)


class CryptoContractResearchTests(unittest.TestCase):
    def test_init_crypto_dossier_creates_protocol_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            dossier = crypto_contract_research.init_crypto_dossier("AERO", root=temp)

            crypto_root = dossier / "crypto"
            self.assertTrue((crypto_root / "artifacts" / "evm").is_dir())
            self.assertTrue((crypto_root / "artifacts" / "solana").is_dir())
            self.assertTrue((crypto_root / "address-registry.csv").exists())
            self.assertTrue((crypto_root / "deployment-matrix.csv").exists())
            self.assertTrue((crypto_root / "security-review.md").exists())
            self.assertTrue((crypto_root / "onchain-forensics.md").exists())
            self.assertTrue((crypto_root / "investment-diligence.md").exists())

            profile = json.loads((crypto_root / "protocol-profile.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["asset"], "AERO")
            self.assertEqual(profile["analysis_mode"], "crypto_protocol")

    def test_validate_address_registry_rejects_bad_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            registry = Path(temp) / "address-registry.csv"
            self.write_registry(
                registry,
                [
                    {
                        "chain": "ethereum",
                        "address": "",
                        "address_type": "token",
                        "source_url": "",
                        "confidence": "certain",
                    }
                ],
            )

            errors = crypto_contract_research.validate_address_registry(registry)
            self.assertIn("line 2: address is required", errors)
            self.assertIn("line 2: invalid confidence 'certain'", errors)
            self.assertIn("line 2: source_url or artifact_path is required", errors)

    def test_analyze_holders_computes_concentration(self):
        with tempfile.TemporaryDirectory() as temp:
            holders = Path(temp) / "holders.csv"
            holders.write_text(
                "address,balance\n"
                "0x1,50\n"
                "0x2,30\n"
                "0x3,20\n",
                encoding="utf-8",
            )
            out = Path(temp) / "out.json"

            summary = crypto_contract_research.analyze_holders(holders, out, top_n=2)

            self.assertEqual(summary["holder_count"], 3)
            self.assertAlmostEqual(summary["top_n_share"], 0.8)
            self.assertAlmostEqual(summary["hhi"], 0.38)
            self.assertEqual(summary["concentration_risk"], "high")
            self.assertTrue(out.exists())

    def test_analyze_evm_abi_flags_privileged_functions(self):
        abi = [
            {"type": "function", "name": "transfer", "inputs": []},
            {"type": "function", "name": "pause", "inputs": []},
            {"type": "function", "name": "setTaxFee", "inputs": []},
            {"type": "function", "name": "upgradeTo", "inputs": []},
            {"type": "function", "name": "blacklist", "inputs": []},
        ]

        summary = crypto_contract_research.analyze_evm_abi_data(abi)

        self.assertIn("pause", summary["privileged_functions"])
        self.assertIn("setTaxFee", summary["privileged_functions"])
        self.assertIn("upgradeTo", summary["privileged_functions"])
        self.assertIn("blacklist", summary["privileged_functions"])
        self.assertEqual(summary["risk_bucket"], "critical")

    def test_analyze_solana_token_flags_authorities(self):
        metadata = {
            "mint": "So11111111111111111111111111111111111111112",
            "supply": "1000000000",
            "decimals": 9,
            "mint_authority": "Authority111",
            "freeze_authority": "Freeze111",
        }

        summary = crypto_contract_research.analyze_solana_token_data(metadata)

        self.assertEqual(summary["mint_authority_status"], "present")
        self.assertEqual(summary["freeze_authority_status"], "present")
        self.assertEqual(summary["risk_bucket"], "high")

    @staticmethod
    def write_registry(path, rows):
        fieldnames = crypto_contract_research.ADDRESS_REGISTRY_COLUMNS
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                full_row = {field: row.get(field, "") for field in fieldnames}
                writer.writerow(full_row)


if __name__ == "__main__":
    unittest.main()
