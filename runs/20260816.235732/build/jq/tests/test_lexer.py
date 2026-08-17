import json
import subprocess
import unittest
from pathlib import Path

from lexer import Lexer, LexError


ROOT = Path(__file__).resolve().parents[1]


class LexerTests(unittest.TestCase):
    def test_located_tokens_cover_names_formats_and_operators(self):
        tokens = Lexer('foo .bar $x @uri //').tokens()
        self.assertEqual([t.kind for t in tokens], ["IDENT", "FIELD", "BINDING", "FORMAT", "//"])
        self.assertEqual((tokens[1].line, tokens[1].column), (1, 5))

    def test_comments_and_continuation_are_ignored(self):
        self.assertEqual([t.value for t in Lexer('1 # comment\n + 2').tokens()], [1, "+", 2])

    def test_invalid_escape_is_lexical_error(self):
        with self.assertRaises(LexError):
            Lexer(r'"u\vw"').tokens()

    def test_cli_acceptance_literals(self):
        result = subprocess.run([str(ROOT / "jq"), "-c", '"alpha"'], input="null\n", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, json.dumps("alpha", separators=(",", ":")) + "\n")

    def test_cli_acceptance_interpolation(self):
        result = subprocess.run([str(ROOT / "jq"), "-c", r'"value=\(.)"'], input="7\n", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '"value=7"\n')


if __name__ == "__main__":
    unittest.main()
