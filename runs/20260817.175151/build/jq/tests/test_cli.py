import io
import json
import unittest

import jq
from lexer import Lexer, LexerError


class CliEntrypointTests(unittest.TestCase):
    def test_lexer_recognizes_front_tokens(self) -> None:
        kinds = [token.kind for token in Lexer('.foo + $value | [., "text", @json]').tokenize()]
        self.assertEqual(kinds, ["FIELD", "+", "BINDING", "|", "[", ".", ",", "QQSTRING_START", "QQSTRING_TEXT", "QQSTRING_END", ",", "FORMAT", "]"])

    def test_comments_and_interpolation_execute(self) -> None:
        output = io.StringIO()
        status = jq.run(["-c", '"value=\\(.) # trailing comment'], io.StringIO("7\n"), output)
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue()), "value=7")

    def test_invalid_escape_is_compile_failure(self) -> None:
        with self.assertRaises(LexerError):
            Lexer('"u\\vw"').tokenize()
        self.assertEqual(jq.run(["-c", '"u\\vw"'], io.StringIO("null\n"), io.StringIO()), 3)

    def test_identity_round_trip(self) -> None:
        payload = {"name": "jq", "items": [1, 2, 3]}
        output = io.StringIO()

        status = jq.run(["-c", "."], io.StringIO(json.dumps(payload) + "\n"), output)

        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue()), payload)

    def test_identity_emits_one_result_per_input(self) -> None:
        values = [1, {"a": 2}, [3, 4]]
        output = io.StringIO()

        status = jq.run(
            ["-c", "."],
            io.StringIO("\n".join(json.dumps(value) for value in values) + "\n"),
            output,
        )

        self.assertEqual(status, 0)
        self.assertEqual([json.loads(line) for line in output.getvalue().splitlines()], values)

    def test_invalid_program_is_compile_failure(self) -> None:
        self.assertEqual(jq.run(["-c", "not-jq"], io.StringIO(), io.StringIO()), 3)

    def test_invalid_json_is_runtime_failure(self) -> None:
        self.assertEqual(jq.run(["-c", "."], io.StringIO("{"), io.StringIO()), 5)

    def test_error_filter_is_runtime_failure(self) -> None:
        output = io.StringIO()

        status = jq.run(["-c", "error"], io.StringIO("null\n"), output)

        self.assertEqual(status, 5)
        self.assertEqual(output.getvalue(), "")

    def test_runtime_failure_preserves_prior_output(self) -> None:
        output = io.StringIO()

        status = jq.run(["-c", "1, error"], io.StringIO("null\n"), output)

        self.assertEqual(status, 5)
        self.assertEqual([json.loads(line) for line in output.getvalue().splitlines()], [1])


if __name__ == "__main__":
    unittest.main()
