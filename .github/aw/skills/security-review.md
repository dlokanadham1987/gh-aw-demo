---
name: security-review
description: Reusable security review checklist for FastAPI / Python services.
  Imported by agentic workflows to keep the same review heuristics in one place.
---

# Security Review Skill

When asked to perform a security review of a code change, apply the checklist
below. The checklist is opinionated for **Python / FastAPI** services like the
`gh-aw-demo` Mini Notes API.

For every finding you raise, use this exact format:

```
- 🔴/🟡/🟢 **<one-line title>** — `<file>:<line>`
  <one sentence explaining the risk>
  <one sentence with a concrete fix>
```

## Severity scale

- 🔴 **High** — exploitable today, or violates an explicit security boundary
  (auth bypass, secret exposure, SQL/command injection, SSRF, path traversal,
  deserialization of untrusted input).
- 🟡 **Medium** — weakens the security posture but needs a chained condition
  (missing input validation, overly broad CORS, weak rate limiting, verbose
  error messages that leak internals).
- 🟢 **Low** — hygiene / hardening suggestion (logging PII, missing security
  headers, dependency pinning, `# nosec` or `# noqa` without justification).

## What to look for

### 1. Input handling
- New endpoints without Pydantic models or with `dict` / `Any` request bodies.
- Path parameters not validated (e.g. `note_id: int` is fine, `note_id: str`
  used as a filesystem path is not).
- Query parameters used in shell commands, SQL, file paths, or `eval`.
- Missing length / range limits on user-controlled strings.

### 2. Authn / authz
- Endpoints that bypass an existing auth dependency (e.g. missing
  `Depends(...)` where peers have one).
- Hardcoded tokens, API keys, or `Authorization: Bearer ...` literals.
- Role checks done in the route handler instead of a dependency
  (easy to forget on the next endpoint).

### 3. Data exposure
- Endpoints that return full ORM / Pydantic objects when only a subset is
  needed (over-fetching → accidental field leak).
- `print(...)` / `logger.info(...)` of request bodies, headers, tokens.
- Stack traces returned to the client (FastAPI default is fine; custom
  handlers that echo `repr(exc)` are not).

### 4. Dependencies & supply chain
- New `requirements.txt` entries pinned to floating versions (`>=`, `*`).
- New imports from packages not already in `requirements.txt`.
- `pip install` invocations inside application code.

### 5. Secrets & config
- `.env`, `*.pem`, `*.key`, `id_rsa`, `secrets.json` added to the diff.
- Secret-looking literals in code (long base64, `AKIA…`, `ghp_…`, `sk-…`).
- New CI workflows that print `${{ secrets.* }}` to logs.

### 6. CI / workflow changes
- Changes under `.github/workflows/` that add `pull_request_target`,
  `workflow_run`, or set `permissions:` to `write-all`.
- New `actions/checkout` with `ref: ${{ github.event.pull_request.head.ref }}`
  combined with privileged token usage.

## Output contract

Always finish with a one-line verdict:

- `✅ No security concerns found.` — if the checklist surfaced nothing.
- `⚠️ <N> findings — see above.` — otherwise, where N is the total count.
