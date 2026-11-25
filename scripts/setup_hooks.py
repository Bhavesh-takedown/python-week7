"""Enable this project's Git hooks on Windows, macOS, and Linux."""

import os
from pathlib import Path
import subprocess


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=repo_root,
        check=True,
    )
    if os.name == "posix":
        for hook_name in ("pre-commit", "commit-msg"):
            hook_path = repo_root / ".githooks" / hook_name
            hook_path.chmod(hook_path.stat().st_mode | 0o111)
    print("Git hooks enabled for this repository.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
