#!/usr/bin/env python3
"""Assemble codex-machinae.md from the playbook/ sources.

The files under playbook/ are the source of truth. The monolithic
codex-machinae.md at the repository root is a generated artefact produced by
plain byte-for-byte concatenation of the sources in MANIFEST order.

Usage:
    python tools/build.py          # regenerate codex-machinae.md
    python tools/build.py --check  # verify codex-machinae.md matches sources
                                   # (exit 0 = in sync, exit 1 = stale/missing)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "codex-machinae.md"

MANIFEST = [
    "playbook/00-frontmatter.md",
    "playbook/core.md",
    "playbook/domains/00-intro.md",
    "playbook/domains/D1-web-service.md",
    "playbook/domains/D2-library-sdk.md",
    "playbook/domains/D3-cli-tool.md",
    "playbook/domains/D4-embedded-firmware.md",
    "playbook/domains/D5-ml-data-pipeline.md",
    "playbook/domains/D6-mobile-app.md",
    "playbook/domains/D7-static-site.md",
    "playbook/modules/00-intro.md",
    "playbook/modules/M1-surveillance.md",
    "playbook/modules/M2-security-sensitive.md",
    "playbook/modules/M3-release-distribution.md",
    "playbook/modules/M4-classification-taxonomy.md",
    "playbook/limitations.md",
    "playbook/appendices/A-checklists.md",
    "playbook/appendices/B-templates.md",
    "playbook/appendices/C-glossary.md",
    "playbook/appendices/D-tooling.md",
]


def assemble() -> bytes:
    chunks = []
    missing = [p for p in MANIFEST if not (ROOT / p).is_file()]
    if missing:
        for p in missing:
            print(f"ERROR: missing source file: {p}", file=sys.stderr)
        sys.exit(1)
    for p in MANIFEST:
        data = (ROOT / p).read_bytes()
        if not data.strip():
            print(f"ERROR: source file is empty: {p}", file=sys.stderr)
            sys.exit(1)
        if not data.endswith(b"\n"):
            print(f"ERROR: source file lacks trailing newline: {p}",
                  file=sys.stderr)
            sys.exit(1)
        chunks.append(data)
    return b"".join(chunks)


def main() -> None:
    check = "--check" in sys.argv[1:]
    assembled = assemble()

    if check:
        if not OUTPUT.is_file():
            print(f"STALE: {OUTPUT.name} does not exist — run tools/build.py")
            sys.exit(1)
        if OUTPUT.read_bytes() != assembled:
            print(f"STALE: {OUTPUT.name} does not match playbook/ sources — "
                  "run tools/build.py and commit the result")
            sys.exit(1)
        print(f"OK: {OUTPUT.name} is in sync with playbook/ sources "
              f"({len(MANIFEST)} files, {len(assembled):,} bytes)")
        return

    OUTPUT.write_bytes(assembled)
    print(f"Wrote {OUTPUT.name} ({len(assembled):,} bytes) "
          f"from {len(MANIFEST)} source files")


if __name__ == "__main__":
    main()
