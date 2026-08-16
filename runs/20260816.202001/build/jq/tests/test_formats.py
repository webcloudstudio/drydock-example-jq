import json
import subprocess
import unittest


class FormatTests(unittest.TestCase):
    def run_jq(self, program: str, value: object) -> list[object]:
        result = subprocess.run(
            ["./jq", "-c", program], input=json.dumps(value) + "\n",
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return [json.loads(line) for line in result.stdout.splitlines()]

    def test_interpolation_preserves_generator_order(self) -> None:
        self.assertEqual(self.run_jq('"x\\(., .)"', 3), ["x3", "x3"])

    def test_format_string_escapes_only_interpolations(self) -> None:
        self.assertEqual(
            self.run_jq('@uri "https://example.test/?q=\\(.)"', "a b?"),
            ["https://example.test/?q=a%20b%3F"],
        )

    def test_public_formats(self) -> None:
        self.assertEqual(self.run_jq("@html", "<x>&'\""), ["&lt;x&gt;&amp;&apos;&quot;"])
        self.assertEqual(self.run_jq("@base64 | @base64d", "round trip"), ["round trip"])
        self.assertEqual(self.run_jq("@csv", ["a", 'b"c', None]), ['a,"b""c",'])
        self.assertEqual(self.run_jq("@tsv", ["a\nb", "c\td"]), ["a\\nb\tc\\td"])
        self.assertEqual(self.run_jq("@sh", ["a", "O'Hara"]), ["'a' 'O'\\''Hara'"])

    def test_json_format_maps_non_finite_numbers_to_null(self) -> None:
        self.assertEqual(self.run_jq("@json", float("nan")), ["null"])

    def test_invalid_format_input_is_runtime_failure(self) -> None:
        result = subprocess.run(
            ["./jq", "-c", "@csv"], input="1\n", capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 5)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
