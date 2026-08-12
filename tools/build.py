#!/usr/bin/env python3
"""Assemble the generated artefacts from the playbook/ sources.

The files under playbook/ are the source of truth. Two artefacts are
generated from them:

1. codex-machinae.md — the monolith at the repository root, produced by
   plain byte-for-byte concatenation of the sources in MANIFEST order.
2. skills/codex-machinae/reference/ — the agent skill's disclosed-reference
   tree, byte-for-byte copies of every source except the monolith-only
   files (frontmatter and part intros). The skill's SKILL.md is authored
   by hand and is not touched by this script.

Usage:
    python tools/build.py          # regenerate both artefacts
    python tools/build.py --check  # verify both match the sources
                                   # (exit 0 = in sync, exit 1 = stale/missing)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "codex-machinae.md"
SKILL_REF = ROOT / "skills" / "codex-machinae" / "reference"

# Monolith-only sources: assembly scaffolding with no standalone value
# inside the skill's reference tree.
SKILL_EXCLUDE = {
    "playbook/00-frontmatter.md",
    "playbook/domains/00-intro.md",
    "playbook/modules/00-intro.md",
}

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


def skill_mapping() -> dict:
    """Map each shared source to its path inside the skill reference tree."""
    return {
        p: SKILL_REF / p.removeprefix("playbook/")
        for p in MANIFEST
        if p not in SKILL_EXCLUDE
    }


def check_skill_tree() -> bool:
    ok = True
    for src, dst in skill_mapping().items():
        if not dst.is_file():
            print(f"STALE: {dst.relative_to(ROOT)} missing — run tools/build.py")
            ok = False
        elif dst.read_bytes() != (ROOT / src).read_bytes():
            print(f"STALE: {dst.relative_to(ROOT)} does not match {src} — "
                  "run tools/build.py and commit the result")
            ok = False
    return ok


def write_skill_tree() -> int:
    count = 0
    for src, dst in skill_mapping().items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ROOT / src).read_bytes())
        count += 1
    return count


def main() -> None:
    check = "--check" in sys.argv[1:]
    assembled = assemble()

    if check:
        ok = True
        if not OUTPUT.is_file():
            print(f"STALE: {OUTPUT.name} does not exist — run tools/build.py")
            ok = False
        elif OUTPUT.read_bytes() != assembled:
            print(f"STALE: {OUTPUT.name} does not match playbook/ sources — "
                  "run tools/build.py and commit the result")
            ok = False
        else:
            print(f"OK: {OUTPUT.name} is in sync with playbook/ sources "
                  f"({len(MANIFEST)} files, {len(assembled):,} bytes)")
        if check_skill_tree():
            print(f"OK: skill reference tree is in sync "
                  f"({len(skill_mapping())} files)")
        else:
            ok = False
        if not ok:
            sys.exit(1)
        return

    OUTPUT.write_bytes(assembled)
    print(f"Wrote {OUTPUT.name} ({len(assembled):,} bytes) "
          f"from {len(MANIFEST)} source files")
    copied = write_skill_tree()
    print(f"Wrote {copied} skill reference files under "
          f"{SKILL_REF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
