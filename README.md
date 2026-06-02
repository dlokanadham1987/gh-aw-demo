# gh-aw-demo — Mini Notes API

A tiny FastAPI sample used to demo **GitHub Agentic Workflows** (gh-aw).

The application itself is intentionally minimal — the main attraction is the
agentic workflow in [.github/workflows/pr-summarizer.md](.github/workflows/pr-summarizer.md),
which uses Claude to post a structured review comment on every pull request.

## Run locally (optional)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API:
- `GET  /health`
- `POST /notes`            body: `{ "title": "...", "body": "..." }`
- `GET  /notes`
- `GET  /notes/{id}`

## Tests

```bash
pytest -q
```

## The agentic workflow

See `.github/workflows/pr-summarizer.md`. On every PR, Claude reads the diff
and posts a single comment with: *What changed*, *Files touched*, *Risk
callouts*, *Test coverage*, *Suggested next steps for reviewers*.
