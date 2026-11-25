# Python Week 7 — Full Gitflow Simulation

This repository contains a mini project for practicing the Gitflow lifecycle: feature branch → pull request → merge → release → hotfix. It also includes a release-notes CLI, local Git hooks, GitHub Actions CI, and a disposable local history simulation.

## Branch model

| Branch | Purpose |
| --- | --- |
| `main` | Production-ready code and tagged releases such as `v1.0.0` |
| `develop` | Integration branch for completed features |
| `feature/*` | New work branched from `develop`, reviewed through a PR back to `develop` |
| `release/*` | Release preparation branched from `develop`, merged into `main` and back into `develop` |
| `hotfix/*` | Urgent production fix branched from `main`, merged into `main` and back into `develop` |

## Get started

Requirements: Python 3.10 or newer and Git.

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -r requirements.txt
python scripts/simulate_gitflow.py
```

The simulation creates a temporary repository, demonstrates a feature PR-style merge, a release, and a hotfix, and prints the commit graph. It does not modify this repository or contact GitHub.

## Release-notes helper

```bash
python -m pip install -e .
gitflow-notes --tag v1.2.0 "feat(cli): add search" "fix: handle an empty query"
```

## Gitflow lifecycle

1. Create `feature/<name>` from `develop`, commit the change, push it, and open a PR back to `develop`.
2. Review the diff, address feedback, and merge after CI and required approvals pass.
3. Create `release/<version>` from `develop`; prepare the version and changelog. Review a PR into `main`, tag the merged production commit, then merge the release branch back into `develop`.
4. Create `hotfix/<version>` from `main`; open a PR into `main`, tag the fix after merge, and merge it back into `develop`.

See [docs/week-7-git-guide.md](docs/week-7-git-guide.md) for branching, conflicts, stash, pull request reviews, rebase, interactive rebase, and cherry-pick.

## Checks and automation

- `.githooks/pre-commit` blocks direct commits on `main` and `develop`, then runs flake8 and pytest.
- `.githooks/commit-msg` enforces Conventional Commit subjects.
- `.github/workflows/ci.yml` runs lint and tests on branch pushes and pull requests to `main` or `develop`.
- `.github/workflows/release.yml` publishes a GitHub Release when a `v*` tag is pushed.

Enable hooks with `python scripts/setup_hooks.py`. GitHub branch protection and CI are the shared safeguards; local hooks can be bypassed with `--no-verify`.
