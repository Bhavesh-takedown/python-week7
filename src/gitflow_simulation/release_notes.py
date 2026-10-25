"""Turn Conventional Commit messages into a compact Markdown changelog."""

from collections import defaultdict
from collections.abc import Iterable
import re

_COMMIT_PATTERN = re.compile(
    r"^(?P<kind>[a-z]+)(?:\([^()]+\))?(?P<breaking>!)?:\s+(?P<subject>.+)$"
)
_CATEGORY_BY_KIND = {
    "feat": "Features",
    "fix": "Fixes",
    "perf": "Performance",
    "docs": "Maintenance",
    "refactor": "Maintenance",
    "style": "Maintenance",
    "test": "Maintenance",
    "build": "Maintenance",
    "ci": "Maintenance",
    "chore": "Maintenance",
}
_CATEGORY_ORDER = ("Breaking Changes", "Features", "Fixes", "Performance", "Maintenance")


def _parse_commit(message: str) -> tuple[str, str]:
    """Return the release-note category and subject for one commit message."""
    lines = message.strip().splitlines()
    if not lines or not lines[0].strip():
        raise ValueError("commit messages must not be empty")

    first_line = lines[0].strip()
    match = _COMMIT_PATTERN.match(first_line)
    breaking_footer = any(
        line.strip().startswith("BREAKING CHANGE:") for line in lines[1:]
    )
    if match is None:
        return "Maintenance", first_line
    if match.group("breaking") or breaking_footer:
        return "Breaking Changes", match.group("subject")

    category = _CATEGORY_BY_KIND.get(match.group("kind"), "Maintenance")
    return category, match.group("subject")


def build_release_notes(tag: str, commit_messages: Iterable[str]) -> str:
    """Build release notes grouped by change type.

    Messages follow the Conventional Commits form, for example feat: add search.
    Unrecognized message types are kept under Maintenance instead of being discarded.
    """
    normalized_tag = tag.strip()
    if not normalized_tag or "\n" in normalized_tag or "\r" in normalized_tag:
        raise ValueError("tag must be a non-empty single line")

    grouped: dict[str, list[str]] = defaultdict(list)
    for message in commit_messages:
        category, subject = _parse_commit(message)
        grouped[category].append(subject)

    lines = [f"# Release {normalized_tag}"]
    for category in _CATEGORY_ORDER:
        subjects = grouped.get(category, [])
        if subjects:
            lines.extend(("", f"## {category}"))
            lines.extend(f"- {subject}" for subject in subjects)
    return "\n".join(lines)
