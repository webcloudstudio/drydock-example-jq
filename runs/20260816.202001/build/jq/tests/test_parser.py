import unittest

import jq_parser


class ParserTests(unittest.TestCase):
    def test_parser_builds_ast(self) -> None:
        ast = jq_parser.parse(".foo | .bar")
        self.assertIsNotNone(ast)
        self.assertEqual(ast.kind, "|")

    def test_parser_preserves_precedence(self) -> None:
        ast = jq_parser.parse("1 + 2 * 2")
        self.assertIn("1", repr(ast))
        self.assertIn("2", repr(ast))
        self.assertEqual(ast.kind, "+")
        self.assertEqual(ast.children[1].kind, "*")

    def test_parser_supports_constructors(self) -> None:
        for program in ("[.foo, .bar]", "{foo: .bar}", "if . then 1 else 2 end"):
            self.assertIsNotNone(jq_parser.parse(program))

    def test_parser_rejects_malformed_program(self) -> None:
        with self.assertRaises(jq_parser.ParseError):
            jq_parser.parse("{")

    def test_parser_supports_generator_and_control_forms(self) -> None:
        for program in (
            ".[] | .name?", ".[-2:]", '"value=\\(.)"',
            ". as $x | $x + 1", "reduce .[] as $x (0; . + $x)",
            "foreach .[] as $x (0; . + $x; .)",
        ):
            self.assertIsNotNone(jq_parser.parse(program))

    def test_parser_rejects_undefined_binding(self) -> None:
        with self.assertRaises(jq_parser.ParseError):
            jq_parser.parse("$missing")

    def test_parser_ast_is_immutable(self) -> None:
        ast = jq_parser.parse("1")
        with self.assertRaises(AttributeError):
            ast.kind = "changed"


if __name__ == "__main__":
    unittest.main()
