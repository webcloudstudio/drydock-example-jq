#!/usr/bin/env python3
"""Render the pinned jq manual into the kit's plain-text specification.

Why plain text and not Markdown. Drydock promotes only non-Markdown imports onto disk in the
build directory; an imported ``.md`` file reaches ``analyze`` and ``plan`` and then disappears,
surviving only as whatever those commands rewrote into the Blueprint. The jq manual is the
normative semantics of every builtin, and a build story that cannot re-read it is working from
a paraphrase. Shipping it as ``.txt`` keeps it both injectable as prose and physically present
in ``sources/`` at build time. This mirrors the CommonMark kit's ``spec.txt``.

The transformation is deterministic and lossless over the language: every section title, entry
title, body, and worked example is preserved verbatim in document order. Two sections are
dropped, both describing the command-line program rather than the language: ``Invoking jq``
(option reference) and ``Colors`` (output colouring). This kit fixes the program's interface in
``INSTRUCTIONS.md`` and exercises no jq option but ``-c``, so neither section is under test.
The manpage intro and epilogue are dropped for the same reason.

Usage:
    python3 tools/render_manual.py            # tools/manual.yml -> sources/jq-manual.txt
    python3 tools/render_manual.py --check    # fail if the rendered file is out of date

Requires PyYAML. This is one-off kit authoring tooling; it is not declared in ``uat.json``, is
never imported by Drydock, and adds no package dependency.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

KIT = Path(__file__).resolve().parent.parent
MANUAL_YML = KIT / "tools" / "manual.yml"
OUTPUT = KIT / "sources" / "jq-manual.txt"

#: Sections describing the command-line program rather than the jq language.
DROPPED_SECTIONS = ("Invoking jq", "Colors")

HEADER = """\
The jq Language Manual
======================

Rendered from the jq manual at tag jq-1.8.2 (docs/content/manual/v1.8/manual.yml).
See PROVENANCE.md for the upstream hash.

This is the normative description of the jq language and is the primary specification
for this project. Section and entry titles, prose, and worked examples are upstream's,
verbatim and in document order. The manual's "Invoking jq" and "Colors" sections are
omitted: they describe jq's command-line option surface, which this project does not
implement and the conformance corpus does not exercise.

Worked examples read:

    Example: <the jq program>
      Input: <the JSON input>
     Output: <each JSON value the program produces, one per line>

"""


def render(document: dict) -> str:
    out: list[str] = [HEADER]

    body = (document.get("body") or "").strip("\n")
    if body:
        out.append("Introduction\n" + "-" * 12 + "\n")
        out.append(body + "\n")

    for section in document.get("sections") or []:
        title = (section.get("title") or "").strip()
        if title in DROPPED_SECTIONS:
            continue
        out.append("\n\n" + "=" * 76)
        out.append(f"SECTION: {title}")
        out.append("=" * 76 + "\n")

        section_body = (section.get("body") or "").strip("\n")
        if section_body:
            out.append(section_body + "\n")

        for entry in section.get("entries") or []:
            entry_title = (entry.get("title") or "").strip()
            out.append("\n" + "-" * 76)
            out.append(entry_title)
            out.append("-" * 76 + "\n")

            entry_body = (entry.get("body") or "").strip("\n")
            if entry_body:
                out.append(entry_body + "\n")

            for example in entry.get("examples") or []:
                out.append(_render_example(example))

    return "\n".join(out).rstrip("\n") + "\n"


def _render_example(example: dict) -> str:
    program = str(example.get("program", ""))
    supplied = str(example.get("input", ""))
    outputs = example.get("output") or []
    lines = [f"    Example: {program}", f"      Input: {supplied}"]
    if not outputs:
        lines.append("     Output: (no output)")
    else:
        lines.append(f"     Output: {outputs[0]}")
        lines.extend(f"             {value}" for value in outputs[1:])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the rendered file differs from what would be written",
    )
    args = parser.parse_args(argv)

    if not MANUAL_YML.is_file():
        print(f"error: {MANUAL_YML} is missing; run tools/fetch_upstream.sh", file=sys.stderr)
        return 2

    text = render(yaml.safe_load(MANUAL_YML.read_text(encoding="utf-8")))

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else ""
        if current != text:
            print(f"error: {OUTPUT.name} is out of date; re-run without --check", file=sys.stderr)
            return 1
        print(f"{OUTPUT.name} is up to date ({len(text)} bytes)")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
