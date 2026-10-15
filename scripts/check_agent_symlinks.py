#!/usr/bin/env python3
"""Verify Claude compatibility paths point at canonical agent files.

Local skills live in `.agents/skills/<name>/`, and Claude reaches each one through
a `SKILL.md` symlink. Vendored skills are `.agents/skills/<name>` directory symlinks
into a git submodule under `vendor/`, and Claude reaches each one through a
directory symlink, so the skill's reference files come along.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_LINKS = {ROOT / "CLAUDE.md": "AGENTS.md"}


def check_link(path: Path, expected_target: str, failures: list[str]) -> None:
    if not path.is_symlink():
        failures.append(f"{path.relative_to(ROOT)} is not a symlink")
        return

    actual_target = os.readlink(path)
    if actual_target != expected_target:
        failures.append(
            f"{path.relative_to(ROOT)} points to {actual_target!r}, expected {expected_target!r}"
        )


def main() -> int:
    failures: list[str] = []

    for path, expected_target in EXPECTED_LINKS.items():
        check_link(path, expected_target, failures)

    for skill in sorted((ROOT / ".agents" / "skills").iterdir()):
        name = skill.name
        if skill.is_symlink():
            if not (skill / "SKILL.md").is_file():
                failures.append(
                    f".agents/skills/{name} points to missing {os.readlink(skill)!r}; run `git submodule update --init`"
                )
            check_link(ROOT / ".claude" / "skills" / name, f"../../.agents/skills/{name}", failures)
        elif (skill / "SKILL.md").is_file():
            check_link(
                ROOT / ".claude" / "skills" / name / "SKILL.md",
                f"../../../.agents/skills/{name}/SKILL.md",
                failures,
            )

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("agent compatibility symlinks are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
