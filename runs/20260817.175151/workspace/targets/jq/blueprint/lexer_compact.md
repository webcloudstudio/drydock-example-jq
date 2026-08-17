<!-- Compacted from lexer.l sha256=cfb3af17a786df30d7e30dae5861b84747d4904f8ce7ae9ab9b48bde342ee7f3 on 2026-08-17 by drydock build agent -->

Lex jq source into tokens for keywords, operators, delimiters, numbers, identifiers, fields, bindings, formats, strings, escapes, interpolation, and comments. Reject invalid escapes/characters and preserve line/column locations.
