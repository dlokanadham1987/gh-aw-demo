---
name: PR Summarizer
on:
  pull_request:
    types: [opened, reopened, synchronize, ready_for_review]
  workflow_dispatch:
    inputs:
      pr_number:
        description: "PR number to summarize (for manual testing)"
        required: true

permissions:
  contents: read
  pull-requests: read

engine: claude

tools:
  bash: [":*"]
  github:
    allowed:
      - get_pull_request
      - get_pull_request_files
      - get_pull_request_diff
      - list_commits
      - get_file_contents

safe-outputs:
  add-comment:
    max: 1
---

# PR Summarizer

You are reviewing a pull request in the `gh-aw-demo` repository, a small
FastAPI "Mini Notes" service used to demonstrate GitHub Agentic Workflows.

The codebase layout is:
- `app/main.py` — FastAPI routes (`/health`, `/notes`)
- `app/models.py` — Pydantic models (`NoteIn`, `Note`)
- `app/store.py` — in-memory store (`NoteStore`, singleton `store`)
- `tests/test_notes.py` — pytest + FastAPI TestClient

## Your task

1. Use the `github` tool to fetch:
   - PR metadata (title, body, author, base/head branch)
   - The full list of changed files and their diff
   - The commit messages

2. Produce ONE markdown comment with the following sections:

### What changed
2–3 sentences in plain English describing the intent of the PR.
Use the commit message subjects and the diff — do not invent.

### Files touched
A grouped bullet list (e.g. `app/`, `tests/`, root) with file counts.
If more than 15 files changed, summarize by directory only.

### Risk callouts
Flag any of these patterns explicitly:
- 🔴 **High** — changes to `app/store.py` data model, removed endpoints,
  or anything that changes the public API shape in `app/main.py`
- 🟡 **Medium** — new endpoints, validation rule changes in `app/models.py`,
  or modifications to error handling
- 🟢 **Low** — tests-only, docs-only, formatting, or pure refactor

### Test coverage
- List any new/modified test files.
- Flag obvious gaps (e.g. new endpoint added but no test references it).
- If only production code changed with no test changes, say so.

### Suggested next steps for reviewers
Up to 3 concrete things a reviewer should check
(e.g. "verify the new `/notes/search` endpoint validates the query param length").

## Rules

- Output ONE comment via the safe-output `add-comment`. Do not
  attempt to comment more than once.
- Do not push code, do not modify files, do not approve the PR.
- Keep the total comment under ~400 words.
- If the diff is empty or trivial (e.g. only whitespace), comment with
  just: `🤖 Trivial change — no summary needed.`
- Start the comment with the header `## 🤖 PR Summary`.
