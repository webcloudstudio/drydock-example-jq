import unittest

import jq_lexer


class LexerTests(unittest.TestCase):
    def test_basic_source_has_identity_field_number_and_pipe(self) -> None:
        tokens = list(jq_lexer.tokenize(".foo | 42"))
        self.assertGreaterEqual(len(tokens), 4)
        self.assertTrue(all(token.kind for token in tokens))
        self.assertEqual([(token.kind, token.value) for token in tokens[:-1]],
                         [("field", "foo"), ("operator", "|"), ("number", "42")])

    def test_format_token(self) -> None:
        token = jq_lexer.tokenize("@json")[0]
        self.assertEqual((token.kind, token.value), ("format", "json"))

    def test_binding_token(self) -> None:
        token = jq_lexer.tokenize("$item")[0]
        self.assertEqual((token.kind, token.value), ("binding", "item"))

    def test_invalid_escape_is_rejected(self) -> None:
        with self.assertRaises(jq_lexer.LexError):
            jq_lexer.tokenize(r'"u\vw"')

    def test_interpolation_and_comment_continuation(self) -> None:
        tokens = jq_lexer.tokenize('"value=\\(.)" # ignored \\\n+  still ignored\n')
        self.assertEqual([token.kind for token in tokens],
                         ["qqstring_start", "qqstring_text", "interpolation_start",
                          "operator", "interpolation_end", "qqstring_end", "eof"])

    def test_mismatched_delimiter_is_rejected(self) -> None:
        with self.assertRaises(jq_lexer.LexError):
            jq_lexer.tokenize("[1}")


if __name__ == "__main__":
    unittest.main()
