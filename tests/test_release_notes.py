"""Tests for release-note grouping and validation."""

import pytest

from gitflow_simulation.release_notes import build_release_notes


def test_groups_changes_in_a_stable_order():
    notes = build_release_notes(
        "v1.2.0",
        ["fix: close the session", "feat(cli): add search", "docs: explain setup"],
    )

    assert notes == (
        "# Release v1.2.0\n\n"
        "## Features\n- add search\n\n"
        "## Fixes\n- close the session\n\n"
        "## Maintenance\n- explain setup"
    )


def test_marks_bang_and_footer_breaking_changes():
    notes = build_release_notes(
        "v2.0.0",
        [
            "feat(api)!: remove legacy endpoint",
            "refactor: change config\n\nBREAKING CHANGE: rename key",
        ],
    )

    assert "## Breaking Changes\n- remove legacy endpoint\n- change config" in notes
    assert "## Features" not in notes


def test_keeps_unknown_commit_types_as_maintenance():
    notes = build_release_notes("v1.0.0", ["Merge pull request #7 from feature/login"])

    assert "## Maintenance\n- Merge pull request #7 from feature/login" in notes


@pytest.mark.parametrize("tag", ["", "  ", "v1.0.0\nextra"])
def test_rejects_empty_or_multiline_tags(tag):
    with pytest.raises(ValueError, match="tag must be a non-empty single line"):
        build_release_notes(tag, [])


def test_rejects_an_empty_commit_message():
    with pytest.raises(ValueError, match="commit messages must not be empty"):
        build_release_notes("v1.0.0", ["  \n"])


def test_header_is_returned_when_there_are_no_changes():
    assert build_release_notes("v1.0.0", []) == "# Release v1.0.0"
