# gh-aw-demo — Mini Notes API

A tiny FastAPI sample used to demo **GitHub Agentic Workflows** (gh-aw).

The application itself is intentionally minimal — the main attraction is the
agentic workflow in [.github/workflows/pr-summarizer.md](.github/workflows/pr-summarizer.md),
which uses Claude to post a structured review comment on every pull request.

---

## Run locally on Windows

You have three options. Pick whichever you like.

### Option 1 — One-click launcher (easiest)

Just double-click **`run.bat`** in this folder.

It creates the venv, installs dependencies, and starts the server. On
subsequent runs it skips the install step and starts immediately. Press
**Ctrl+C** in the window to stop.

When the server is up, open:
- API root:    http://127.0.0.1:8000
- Swagger UI:  http://127.0.0.1:8000/docs

### Option 2 — Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Option 3 — PowerShell or CMD

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

> **Note:** the server uses `--reload`, so it auto-restarts whenever you edit
> a Python file. Useful while developing.

---

## Dummy data on startup

The store loads `app/seed.json` automatically on startup, so the API always
has data after a fresh restart. Out of the box you'll see 7 sample notes
covering business + personal topics.

To customise the seed data, edit [`app/seed.json`](app/seed.json) and restart
the server.

To start with an empty store, delete or rename `app/seed.json`.

---

## API endpoints

| Method | Path                       | What it does                              |
|--------|----------------------------|-------------------------------------------|
| GET    | `/health`                  | Liveness probe — `{"status":"ok"}`        |
| POST   | `/notes`                   | Create a note — body: `{"title","body"}`  |
| GET    | `/notes`                   | List all notes                            |
| GET    | `/notes/search?q=<term>`   | Case-insensitive search by title          |
| GET    | `/notes/{id}`              | Get a single note by id (404 if missing)  |

The Swagger UI at `/docs` lets you try every endpoint live in the browser.

---

## Tests

```bash
pytest -q
```

---

## The agentic workflows

This repo is the host for several gh-aw demos:

- [`pr-summarizer.md`](.github/workflows/pr-summarizer.md) — on every PR, Claude
  reads the diff and posts a single structured review comment.

Future demos that will be added:
- `pr-reviewer.md` — finds bugs, security issues, missing validation
- `pr-autofixer.md` — applies the reviewer's suggested fixes (triggered by label)
- `pr-security-reviewer.md` — imports a shared skill from `.claude/skills/`
- `tfs-ticket-researcher.md` — fetches a TFS work item and writes a research doc

See the project's
[deep-dive guide](presentation/github-agentic-workflows-guide.md) for the
concepts and architecture behind these workflows.
