#!/usr/bin/env python3
"""Lightweight repository check for Codex GROMACS skills."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def main() -> int:
    failures = []
    for skill in sorted(SKILLS.iterdir()):
        if not skill.is_dir():
            continue
        doc = skill / "SKILL.md"
        if not doc.exists():
            failures.append(f"{skill.name}: missing SKILL.md")
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
            failures.append(f"{skill.name}: invalid frontmatter")
        if len(text.splitlines()) > 500:
            failures.append(f"{skill.name}: SKILL.md exceeds 500 lines")
        if (skill / "README.md").exists():
            failures.append(f"{skill.name}: README.md should remain at repository root")
    if failures:
        print("STATUS: FAIL")
        print("\n".join(failures))
        return 1
    print(f"STATUS: PASS ({len(list(SKILLS.iterdir()))} skill directories checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
