import io
import unittest

from jq_interpreter.ast import Comma, Identity, Literal, Pipeline
from jq_interpreter.cli import run
from jq_interpreter.errors import COMPILE_ERROR, RUNTIME_ERROR
from jq_interpreter.parser import parse
from jq_interpreter.lexer import tokenize
from jq_interpreter.errors import CompileError


class ArchitectureTests(unittest.TestCase):
    def test_lexer_recognizes_jq_surface_and_locations(self) -> None:
        tokens = tokenize('def f($x): .foo |= $x // 1; # comment\n')
        self.assertEqual([token.kind for token in tokens], [
            "DEF", "IDENT", "LPAREN", "BINDING", "RPAREN", "COLON", "FIELD",
            "SETPIPE", "BINDING", "DEFINEDOR", "NUMBER", "SEMICOLON", "EOF",
        ])
        self.assertEqual(tokens[0].location.line, 1)
        self.assertEqual(tokens[-1].location.line, 2)

    def test_lexer_validates_unicode_and_rejects_bad_escapes(self) -> None:
        self.assertEqual(tokenize('"\\u03bc"')[0].value, '"\\u03bc"')
        with self.assertRaises(CompileError):
            tokenize('"u\\vw"')
        with self.assertRaises(CompileError):
            tokenize("@")

    def test_lexer_comment_continuation_hides_next_line(self) -> None:
        tokens = tokenize("1 # hidden \\\n+2\n3")
        self.assertEqual([token.value for token in tokens], ["1", "3", ""])

    def test_lexer_balances_nested_and_multiple_interpolations(self) -> None:
        tokens = tokenize('"\\(1 + (2 * 3)) / \\(.x)"')
        self.assertEqual(
            [token.kind for token in tokens],
            [
                "QQSTRING_START", "QQSTRING_INTERP_START", "NUMBER", "PLUS",
                "LPAREN", "NUMBER", "MULT", "NUMBER", "RPAREN",
                "QQSTRING_INTERP_END", "QQSTRING_TEXT", "QQSTRING_INTERP_START",
                "FIELD", "QQSTRING_INTERP_END", "QQSTRING_END", "EOF",
            ],
        )

    def test_lexer_does_not_treat_escaped_backslash_as_interpolation(self) -> None:
        tokens = tokenize('"\\\\("')
        self.assertEqual([token.kind for token in tokens], ["STRING", "EOF"])

    def test_lexer_accepts_upstream_numeric_spellings(self) -> None:
        tokens = tokenize("01 2.  .5 1e-3")
        self.assertEqual([token.kind for token in tokens], ["NUMBER"] * 4 + ["EOF"])
        self.assertEqual([token.value for token in tokens[:-1]], ["01", "2.", ".5", "1e-3"])

    def test_lexer_rejects_bad_escape_in_interpolated_string(self) -> None:
        with self.assertRaises(CompileError):
            tokenize('"prefix \\(1) \\v"')

    def test_parser_exposes_ast_boundaries(self) -> None:
        self.assertIsInstance(parse("."), Identity)
        self.assertIsInstance(parse("1, 2"), Comma)
        self.assertIsInstance(parse(". | 1"), Pipeline)
        self.assertIsInstance(parse('"x"'), Literal)

    def test_cli_emits_compact_ordered_values(self) -> None:
        output = io.StringIO()
        status = run(["-c", "., 1"], io.StringIO("{\"a\": 2}\n"), output, io.StringIO())
        self.assertEqual(status, 0)
        self.assertEqual(output.getvalue(), '{"a":2}\n1\n')

    def test_cli_distinguishes_compile_failure(self) -> None:
        self.assertEqual(run(["-c", "!"], io.StringIO(), io.StringIO(), io.StringIO()), COMPILE_ERROR)

    def test_cli_rejects_malformed_string_escape_at_compile_time(self) -> None:
        self.assertEqual(
            run(["-c", '"u\\vw"'], io.StringIO("null\n"), io.StringIO(), io.StringIO()),
            COMPILE_ERROR,
        )

    def test_cli_rejects_malformed_module_metadata_at_compile_time(self) -> None:
        self.assertEqual(
            run(["-c", "module []; 0"], io.StringIO("null\n"), io.StringIO(), io.StringIO()),
            COMPILE_ERROR,
        )

    def test_cli_distinguishes_runtime_input_failure(self) -> None:
        self.assertEqual(run(["-c", "."], io.StringIO("not-json\n"), io.StringIO(), io.StringIO()), RUNTIME_ERROR)


if __name__ == "__main__":
    unittest.main()
