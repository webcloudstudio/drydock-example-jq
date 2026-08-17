import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).parents[1]


class ArchitectureContractTests(unittest.TestCase):
    def run_jq(self, program: str, value: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(ROOT / "jq"), "-c", program],
            input=json.dumps(value) + "\n",
            capture_output=True,
            text=True,
            check=False,
        )

    def test_identity_round_trip(self) -> None:
        payload = {"architecture": ["stream", "generator"]}
        result = self.run_jq(".", payload)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), payload)

    def test_comma_preserves_order_and_multiplicity(self) -> None:
        result = self.run_jq("1, 1, 2", None)
        self.assertEqual(result.returncode, 0)
        self.assertEqual([json.loads(line) for line in result.stdout.splitlines()], [1, 1, 2])

    def test_runtime_failure_status_and_empty_stdout(self) -> None:
        result = self.run_jq("error", None)
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout, "")

    def test_compile_failure_status(self) -> None:
        result = self.run_jq("unknown", None)
        self.assertEqual(result.returncode, 3)


if __name__ == "__main__":
    unittest.main()
