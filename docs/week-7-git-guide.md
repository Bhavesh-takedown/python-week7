# Week 7 Git Guide

This guide pairs the Gitflow project with the fundamentals and intermediate topics in the course outline.

## Start a repository and share it

    git init
    git clone <repository-url>
    git status
    git add <file>
    git commit -m "feat: describe the change"
    git push -u origin <branch>
    git pull --ff-only

git add stages selected changes; git commit records the staged snapshot; git push publishes local commits; and git pull fetches and integrates remote commits. Review git status before staging and committing.

## Create and merge branches

    git switch -c feature/search develop
    # edit files and commit
    git switch develop
    git merge --no-ff feature/search

A fast-forward merge moves the target branch pointer when it has no unique commits. A three-way merge creates a merge commit when both branches advanced from a common ancestor. The --no-ff option records the feature boundary even when fast-forward is possible.

## Resolve a merge conflict

1. Merge the target branch and note the files Git marks as conflicted.
2. Open each file and edit the <<<<<<<, =======, and >>>>>>> sections into the intended final content.
3. Run the project checks, stage the resolved files, and commit the merge.

    git status
    # edit conflicted files and remove the conflict markers
    git add <resolved-file>
    git commit

To abandon the merge before committing, use git merge --abort.

## Stash temporary work

    git stash push -m "work in progress: search"
    git stash list
    git stash apply stash@{0}
    git stash pop

apply restores a stash and keeps its entry; pop restores and removes it. A stash can conflict when applied to a changed branch. Resolve files and inspect git status before continuing.

## Pull request and review

Push a feature branch and open a PR with develop as its base. Explain the problem, summarize the change, and call out testing. Reviewers inspect the diff, leave comments or request changes, and approve when ready. Update the feature branch to address feedback; merge after required reviews and CI checks pass. This project uses merge commits to preserve the PR boundary.

## Rebase versus merge

- Merge preserves the existing branch graph and works well for shared branches and PR integration.
- Rebase replays commits onto a newer base to create a linear history. It changes commit IDs, so rebase only commits that have not been shared with others.

On a private feature branch, git fetch origin followed by git rebase origin/develop can update the branch before review. Resolve conflicts, run checks, then push normally if the branch was never published; coordinate before rewriting published history.

## Interactive rebase

Use git rebase -i <base> only on a private feature branch. The todo list supports pick (keep), reword (change the message), squash (combine with the previous commit and edit the message), fixup (combine and discard the message), and reordering lines. Save and close the editor, resolve conflicts if prompted, then inspect history with git log --oneline.

## Cherry-pick one commit

    git log --oneline <source-branch>
    git switch <target-branch>
    git cherry-pick <commit-sha>

Cherry-pick copies one commit's change onto the current branch as a new commit. Use it for a narrowly scoped fix on a second branch; for a normal feature, prefer merging through its PR.
