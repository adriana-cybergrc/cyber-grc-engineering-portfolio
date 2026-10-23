
import tempfile
import unittest
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "audit_store.py"
spec = spec_from_file_location("audit_store", MODULE_PATH)
audit_store = module_from_spec(spec)
spec.loader.exec_module(audit_store)


class TestAuditStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = str(Path(self.temp_dir.name) / "test_audit.db")
        audit_store.initialize_database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_saves_run_and_findings(self):
        findings = [{
            "control_id": "CTRL002",
            "finding_type": "EVIDENCE_EXPIRED",
            "severity": "HIGH",
            "details": "Synthetic evidence has expired.",
        }]

        run_id = audit_store.save_audit_run(self.db_path, 5, findings)
        history = audit_store.get_audit_history(self.db_path)
        saved_findings = audit_store.get_findings_for_run(
            self.db_path, run_id
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["controls_evaluated"], 5)
        self.assertEqual(history[0]["findings_count"], 1)
        self.assertEqual(len(saved_findings), 1)
        self.assertEqual(saved_findings[0]["finding_type"], "EVIDENCE_EXPIRED")

    def test_saves_run_with_no_findings(self):
        run_id = audit_store.save_audit_run(self.db_path, 5, [])
        history = audit_store.get_audit_history(self.db_path)
        saved_findings = audit_store.get_findings_for_run(
            self.db_path, run_id
        )

        self.assertEqual(history[0]["findings_count"], 0)
        self.assertEqual(saved_findings, [])


if __name__ == "__main__":
    unittest.main()
