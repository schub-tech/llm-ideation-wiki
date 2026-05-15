#!/usr/bin/env python3
"""Verify Claude compatibility paths point at canonical agent files."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_LINKS = {ROOT / "CLAUDE.md": "AGENTS.md"}


def main() -> int:
    failures: list[str] = []
    canonical_skills = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))

    for path, expected_target in EXPECTED_LINKS.items():
        if not path.is_symlink():
            failures.append(f"{path.relative_to(ROOT)} is not a symlink")
            continue

        actual_target = os.readlink(path)
        if actual_target != expected_target:
            failures.append(
                f"{path.relative_to(ROOT)} points to {actual_target!r}, expected {expected_target!r}"
            )

    for canonical_skill in canonical_skills:
        skill_name = canonical_skill.parent.name
        path = ROOT / ".claude" / "skills" / skill_name / "SKILL.md"
        expected_target = f"../../../.agents/skills/{skill_name}/SKILL.md"

        if not path.is_symlink():
            failures.append(f"{path.relative_to(ROOT)} is not a symlink")
            continue

        actual_target = os.readlink(path)
        if actual_target != expected_target:
            failures.append(
                f"{path.relative_to(ROOT)} points to {actual_target!r}, expected {expected_target!r}"
            )

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("agent compatibility symlinks are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
