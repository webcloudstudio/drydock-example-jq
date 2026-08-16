#!/bin/sh
# fetch_upstream.sh — acquire the pinned jq upstream assets for this UAT kit.
#
# The kit's corpus and grammar are upstream artifacts, never Drydock artifacts. This script
# is the only sanctioned way they enter the kit, and it records a sha256 for each so a later
# reader can confirm the exam that was graded is the exam upstream published.
#
# Usage:
#   sh tools/fetch_upstream.sh            # fetch, then write PROVENANCE.md
#   sh tools/fetch_upstream.sh --verify   # re-hash what is on disk; change nothing
#
# Requires network access. Everything after this point is offline.

set -eu

JQ_TAG="jq-1.8.2"
RAW="https://raw.githubusercontent.com/jqlang/jq/${JQ_TAG}"

KIT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="fetch"
[ "${1:-}" = "--verify" ] && MODE="verify"

# upstream path -> destination, relative to the kit root.
set -- \
    "tests/jq.test:sources/jq.test" \
    "src/parser.y:sources/parser.y" \
    "src/lexer.l:sources/lexer.l" \
    "src/builtin.jq:sources/builtin.jq" \
    "docs/content/manual/v1.8/manual.yml:tools/manual.yml" \
    "COPYING:tools/COPYING"

mkdir -p "${KIT}/sources" "${KIT}/tools"

if [ "${MODE}" = "fetch" ]; then
    for pair in "$@"; do
        remote="${pair%%:*}"
        local="${pair#*:}"
        echo "fetch ${remote} -> ${local}"
        curl -fsSL "${RAW}/${remote}" -o "${KIT}/${local}"
    done
fi

if [ "${MODE}" = "verify" ]; then
    OUT="$(mktemp)"
    trap 'rm -f "${OUT}"' EXIT
else
    OUT="${KIT}/PROVENANCE.md"
fi

{
    echo "# Provenance"
    echo
    echo "Upstream: https://github.com/jqlang/jq"
    echo "Tag: ${JQ_TAG}"
    echo "Fetched by: tools/fetch_upstream.sh"
    echo
    echo "Every file below is byte-for-byte upstream. None is hand-edited. Where a case in"
    echo "the corpus cannot run under this kit's harness, the exclusion is declared in"
    echo "\`sources/exclusions.txt\` rather than by modifying the corpus."
    echo
    echo "| Upstream path | Kit path | Bytes | SHA-256 |"
    echo "|---|---|---|---|"
    for pair in "$@"; do
        remote="${pair%%:*}"
        local="${pair#*:}"
        path="${KIT}/${local}"
        [ -f "${path}" ] || { echo "error: missing ${local}" >&2; exit 1; }
        bytes="$(wc -c < "${path}" | tr -d ' ')"
        sum="$(sha256sum "${path}" | cut -d' ' -f1)"
        echo "| \`${remote}\` | \`${local}\` | ${bytes} | \`${sum}\` |"
    done
    echo
    echo "## Derived"
    echo
    echo "\`sources/jq-manual.txt\` is rendered from \`tools/manual.yml\` by"
    echo "\`tools/render_manual.py\`. It is a deterministic transformation: section and entry"
    echo "titles, bodies, and examples are preserved; the \`Invoking jq\` section and the"
    echo "manpage intro and epilogue are dropped, because this kit fixes the program's"
    echo "interface itself and jq's command-line option surface is not under test."
    echo
    echo "\`LICENSE\` is upstream \`COPYING\` with a kit attribution note prepended."
} > "${OUT}"

echo
if [ "${MODE}" = "verify" ]; then
    if diff -u "${KIT}/PROVENANCE.md" "${OUT}"; then
        echo "verified: every file on disk matches PROVENANCE.md"
    else
        echo "error: on-disk files do not match PROVENANCE.md (diff above)" >&2
        exit 1
    fi
else
    echo "wrote ${KIT}/PROVENANCE.md"
fi
