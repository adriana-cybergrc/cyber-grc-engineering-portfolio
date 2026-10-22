import unittest

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "sod_analyzer.py"
)

spec = importlib.util.spec_from_file_location("sod_analyzer", MODULE_PATH)
sod_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sod_analyzer)

analyze_sod = sod_analyzer.analyze_sod


class TestSodAnalyzer(unittest.TestCase):
    def test_detects_vendor_creation_and_payment_approval(self):
        users = [
            {"user_id": "USR001", "business_function": "CREATE_VENDOR"},
            {"user_id": "USR001", "business_function": "APPROVE_PAYMENT"},
        ]
        rules = [
            {
                "rule_id": "SOD001",
                "rule_name": "Vendor Creation vs Payment Approval",
                "function_a": "CREATE_VENDOR",
                "function_b": "APPROVE_PAYMENT",
                "risk_level": "HIGH",
            }
        ]

        findings = analyze_sod(users, rules)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["user_id"], "USR001")
        self.assertEqual(findings[0]["status"], "REQUIRES_REVIEW")

    def test_no_conflict_when_functions_are_separated(self):
        users = [
            {"user_id": "USR001", "business_function": "CREATE_VENDOR"},
            {"user_id": "USR002", "business_function": "APPROVE_PAYMENT"},
        ]
        rules = [
            {
                "rule_id": "SOD001",
                "rule_name": "Vendor Creation vs Payment Approval",
                "function_a": "CREATE_VENDOR",
                "function_b": "APPROVE_PAYMENT",
                "risk_level": "HIGH",
            }
        ]

        self.assertEqual(analyze_sod(users, rules), [])


if __name__ == "__main__":
    unittest.main()
