"""Create a disposable Git repository and walk through a complete Gitflow cycle."""

from pathlib import Path
import subprocess
import tempfile


class GitSimulation:
    """Run Git commands in an isolated temporary repository."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def run(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def write(self, relative_path: str, content: str) -> None:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit_file(self, relative_path: str, content: str, message: str) -> None:
        self.write(relative_path, content)
        self.run("add", relative_path)
        self.run("commit", "-m", message)


def simulate(root: Path) -> str:
    """Build the feature, release, and hotfix history and return its graph."""
    git = GitSimulation(root)
    git.run("init", "--quiet", "--initial-branch=main")
    git.run("config", "user.name", "Gitflow Simulation")
    git.run("config", "user.email", "gitflow@example.invalid")
    git.run("config", "commit.gpgsign", "false")

    git.write("README.md", "Disposable repository used by the Gitflow walkthrough.\n")
    git.write("src/release_notes.py", "def normalize_tag(tag):\n    return tag.strip()\n")
    git.write("VERSION", "0.1.0\n")
    git.run("add", ".")
    git.run("commit", "-m", "chore: create the initial application")
    git.run("switch", "-c", "develop")

    git.run("switch", "-c", "feature/add-release-notes")
    git.commit_file(
        "src/release_notes.py",
        "def normalize_tag(tag):\n    return tag.strip()\n\n"
        "def format_notes(tag):\n    return f\"# Release {tag}\"\n",
        "feat: add release note headings",
    )
    git.run("switch", "develop")
    git.run(
        "merge",
        "--no-ff",
        "-m",
        "Merge pull request #1: add release notes",
        "feature/add-release-notes",
    )

    git.run("switch", "-c", "release/1.0.0")
    git.commit_file("VERSION", "1.0.0\n", "chore(release): prepare v1.0.0")
    git.run("switch", "main")
    git.run("merge", "--no-ff", "-m", "Merge release/1.0.0", "release/1.0.0")
    git.run("tag", "-a", "v1.0.0", "-m", "Release v1.0.0")
    git.run("switch", "develop")
    git.run(
        "merge",
        "--no-ff",
        "-m",
        "Merge release/1.0.0 back into develop",
        "release/1.0.0",
    )

    git.run("switch", "main")
    git.run("switch", "-c", "hotfix/1.0.1")
    git.commit_file(
        "src/release_notes.py",
        "def normalize_tag(tag):\n"
        "    if not tag or not tag.strip():\n"
        "        raise ValueError(\"tag must not be empty\")\n"
        "    return tag.strip()\n\n"
        "def format_notes(tag):\n    return f\"# Release {tag}\"\n",
        "fix: reject an empty release tag",
    )
    git.run("switch", "main")
    git.run("merge", "--no-ff", "-m", "Merge hotfix/1.0.1", "hotfix/1.0.1")
    git.run("tag", "-a", "v1.0.1", "-m", "Release v1.0.1")
    git.run("switch", "develop")
    git.run(
        "merge",
        "--no-ff",
        "-m",
        "Merge hotfix/1.0.1 back into develop",
        "hotfix/1.0.1",
    )

    return git.run("log", "--graph", "--all", "--decorate", "--oneline")


def main() -> int:
    print("Gitflow walkthrough: feature branch → PR-style merge → release → hotfix")
    with tempfile.TemporaryDirectory(prefix="gitflow-simulation-") as temp_dir:
        graph = simulate(Path(temp_dir))
        print("\nSimulated commit graph (the temporary repository is removed on exit):\n")
        print(graph)
    print("\nFeature PR #1 was merged into develop with a merge commit.")
    print("Release v1.0.0 and hotfix v1.0.1 were tagged and back-merged into develop.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
