# Provenance

Upstream: https://github.com/jqlang/jq
Tag: jq-1.8.2
Fetched by: tools/fetch_upstream.sh

Every file below is byte-for-byte upstream. None is hand-edited. Where a case in
the corpus cannot run under this kit's harness, the exclusion is declared in
`sources/exclusions.txt` rather than by modifying the corpus.

| Upstream path | Kit path | Bytes | SHA-256 |
|---|---|---|---|
| `tests/jq.test` | `sources/jq.test` | 52230 | `329689763b651096989bd8260b643731083fc5fd17f6bd7834d158713f738cbd` |
| `src/parser.y` | `sources/parser.y` | 22382 | `803aa7c0b1acba2228e52d1de392fb51e60a7bbe23e42870aea1d62c43360c60` |
| `src/lexer.l` | `sources/lexer.l` | 4548 | `cfb3af17a786df30d7e30dae5861b84747d4904f8ce7ae9ab9b48bde342ee7f3` |
| `src/builtin.jq` | `sources/builtin.jq` | 9631 | `b8a5fd9579be9b51c9a04e6620f8c1655539aa57eea33a84e202a8dea401f2a4` |
| `docs/content/manual/v1.8/manual.yml` | `tools/manual.yml` | 147279 | `2309907188195edee4659ffcdd52d4a30c51d4ef3824a05bcdb9d5e259802a73` |
| `COPYING` | `tools/COPYING` | 7887 | `ad2b4a266b2268939c1446979759706077421cf906a203aa188c6f396e8cfd74` |

## Derived

`sources/jq-manual.txt` is rendered from `tools/manual.yml` by
`tools/render_manual.py`. It is a deterministic transformation: section and entry
titles, bodies, and examples are preserved; the `Invoking jq` section and the
manpage intro and epilogue are dropped, because this kit fixes the program's
interface itself and jq's command-line option surface is not under test.

`LICENSE` is upstream `COPYING` with a kit attribution note prepended.
