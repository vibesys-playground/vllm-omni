#!/usr/bin/env python3
"""Validate the local source inputs required by the Show-o2 task."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = TASK_ROOT.parents[2]
REFERENCE_SUBMODULE = TASK_ROOT / "reference" / "Show-o"
REFERENCE_PATH = REFERENCE_SUBMODULE.relative_to(PROJECT_ROOT)
INITIALIZE_COMMAND = "git submodule update --init --recursive .vibesys/tasks/show-o2-1.5b-hq/reference/Show-o"


def main() -> int:
    """Fail unless the pinned Show-o checkout and its nested submodules exist."""
    status = subprocess.run(
        ["git", "submodule", "status", "--recursive", "--", str(REFERENCE_PATH)],
        cwd=PROJECT_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if status.returncode != 0:
        return _fail(f"could not inspect git submodules: {status.stderr.strip()}")

    lines = tuple(line for line in status.stdout.splitlines() if line)
    invalid = tuple(line for line in lines if line[0] in {"-", "+", "U"})
    required = (
        REFERENCE_SUBMODULE / "show-o2" / "models",
        REFERENCE_SUBMODULE / "show-o2" / "transport",
        REFERENCE_SUBMODULE / "show-o2" / "configs",
    )
    missing = tuple(path for path in required if not path.is_dir())
    if not lines or invalid or missing:
        details: list[str] = []
        if invalid:
            details.append("unexpected submodule status: " + "; ".join(invalid))
        if missing:
            rendered_missing = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
            details.append("missing source directories: " + rendered_missing)
        return _fail("; ".join(details) or "Show-o submodule is not initialized")

    print(f"Show-o reference checkout is ready: {REFERENCE_PATH}")
    return 0


def _fail(reason: str) -> int:
    print(f"Show-o task preflight failed: {reason}", file=sys.stderr)
    print(f"Initialize it with: {INITIALIZE_COMMAND}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
