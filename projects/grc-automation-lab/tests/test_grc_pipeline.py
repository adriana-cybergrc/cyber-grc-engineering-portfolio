
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, call
import subprocess


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "run_grc_pipeline.py"
)

SPEC = importlib.util.spec_from_file_location(
    "run_grc_pipeline", SCRIPT_PATH
)
pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pipeline)


class TestGRCPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.steps = []
        for name in ("audit.py", "analytics.py", "dashboard.py"):
            script = self.root / name
            script.write_text("# test script", encoding="utf-8")
            self.steps.append((name, script))

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch.object(pipeline.subprocess, "run")
    def test_runs_all_steps_when_successful(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0
        )

        with patch.object(pipeline, "PIPELINE_STEPS", self.steps):
            result = pipeline.main()

        self.assertEqual(result, 0)
        self.assertEqual(mock_run.call_count, 3)

    @patch.object(pipeline.subprocess, "run")
    def test_stops_when_a_step_fails(self, mock_run):
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0),
            subprocess.CompletedProcess(args=[], returncode=1),
        ]

        with patch.object(pipeline, "PIPELINE_STEPS", self.steps):
            result = pipeline.main()

        self.assertEqual(result, 1)
        self.assertEqual(mock_run.call_count, 2)

    @patch.object(pipeline.subprocess, "run")
    def test_fails_if_script_is_missing(self, mock_run):
        missing_step = ("missing", self.root / "missing.py")

        with patch.object(
            pipeline, "PIPELINE_STEPS", [missing_step]
        ):
            result = pipeline.main()

        self.assertEqual(result, 1)
        mock_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
