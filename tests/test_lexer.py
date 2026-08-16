import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from jqlang import CompileError, lex


class LexerTests(unittest.TestCase):
    def test_recognizes_keywords_fields_bindings_formats_and_numbers(self):
        kinds = [token.kind for token in lex('def f: .foo | $x + @uri 1.2e-3 # note')]
        self.assertEqual(kinds, ["def", "IDENT", ":", "FIELD", "|", "$", "IDENT", "+", "FORMAT", "NUMBER", "EOF"])

    def test_comments_and_whitespace_are_ignored(self):
        self.assertEqual([token.kind for token in lex("1 # ignored\n + 2")], ["NUMBER", "+", "NUMBER", "EOF"])

    def test_invalid_escape_is_compile_error(self):
        with self.assertRaises(CompileError):
            lex(r'"u\vw"')

    def test_executable_compact_literal_boundary(self):
        result = subprocess.run([str(ROOT / "jq"), "-c", "1"], input="null\n", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual([json.loads(line) for line in result.stdout.splitlines()], [1])


if __name__ == "__main__":
    unittest.main()
