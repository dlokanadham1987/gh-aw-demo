# Deep-Dive — GitHub Agentic Workflows

> **For your personal learning.** This is concept-organized (not slide-by-slide),
> so you can read it as a book. Each chapter is self-contained: definition →
> why it matters → details → common questions → gotchas.
>
> Read it cover-to-cover once. Re-read individual chapters before specific Q&A
> moments. Use the table of contents as your index.

---

## Table of contents

1. [Foundations — GitHub, Actions, gh CLI, gh-aw](#chapter-1--foundations)
2. [What is a "mental model" and why we use the term](#chapter-2--what-is-a-mental-model)
3. [The three layers — the corrected mental model](#chapter-3--the-three-layers)
4. [The two Claudes — a critical point of confusion](#chapter-4--the-two-claudes)
5. [Compile time vs Runtime — the single most important distinction](#chapter-5--compile-time-vs-runtime)
6. [Anatomy of the `.md` file (frontmatter vs body)](#chapter-6--anatomy-of-the-md-file)
7. [Anatomy of the `.lock.yml` (what's really in it)](#chapter-7--anatomy-of-the-lockyml)
8. [Why two files? — the design reasons](#chapter-8--why-two-files)
9. [The runtime lifecycle in detail](#chapter-9--the-runtime-lifecycle-in-detail)
10. [The security model](#chapter-10--the-security-model)
11. [The cast of characters](#chapter-11--the-cast-of-characters)
12. [Terminology cheat-sheet](#chapter-12--terminology-cheat-sheet)
13. [Common misconceptions and corrections](#chapter-13--common-misconceptions-and-corrections)
14. [The practical workflow-author lifecycle](#chapter-14--the-practical-workflow-author-lifecycle)
15. [Things you will inevitably forget](#chapter-15--things-you-will-inevitably-forget)
16. [Appendix A — Pre-demo checklist](#appendix-a--pre-demo-checklist)
17. [Appendix B — FAQ to rehearse before Q&A](#appendix-b--faq-to-rehearse-before-qa)
18. [Appendix C — Further reading & references](#appendix-c--further-reading--references)

---

## Chapter 1 — Foundations

> *Goal: nail down the four words people throw around interchangeably so you can
> separate them confidently in any conversation.*

### 1.1 GitHub

The **website + git hosting service** at `github.com`. Stores your source code,
manages pull requests, issues, releases, users, organizations. Owned by Microsoft
since 2018.

Think of it as the **platform**. It's where your repo lives.

### 1.2 GitHub Actions

A **CI/CD engine** that GitHub built on top of GitHub itself. It watches your
repository for events (a push, a PR, a comment, a schedule, etc.) and, when an
event matches, spins up a virtual machine called a **runner**, clones your repo
onto it, and executes a YAML pipeline you've defined in `.github/workflows/`.

Think of it as **TFS/Jenkins, but native to GitHub**. The pipeline format is YAML.
Runs on GitHub-hosted runners (Linux/Windows/macOS VMs in GitHub's cloud) or on
**self-hosted** runners (machines you own).

### 1.3 The `gh` CLI

GitHub's **official command-line tool**, separate from `git`. It speaks the
GitHub REST/GraphQL API: open PRs, create issues, manage secrets, view workflow
runs — all from your terminal.

- Repo: `github.com/cli/cli`
- Maintained by: GitHub
- Status: GA, stable

You ran `gh auth status` earlier — that was the `gh` CLI authenticating you to GitHub.

### 1.4 The `gh aw` extension (this is gh-aw)

A **plug-in for `gh`** that adds the `aw` subcommand family. "aw" stands for
**Agentic Workflows**.

| Attribute | Detail |
|---|---|
| **Full name** | GitHub Agentic Workflows |
| **Repo** | `github.com/githubnext/gh-aw` |
| **Author** | **GitHub Next** — GitHub's internal research/experimental lab |
| **Ownership chain** | GitHub Next → GitHub → Microsoft |
| **Language** | Go |
| **License** | Open source (verify the exact license on the repo before quoting in your talk) |
| **Status** | **Public preview / experimental** — production-usable but not yet a fully GA product |
| **What it adds** | A way to author GitHub Actions workflows in **Markdown** so AI agents can be safely embedded |

### 1.5 What is GitHub Next?

This matters because someone will ask "is this official?"

GitHub Next is GitHub's **R&D division** — they incubate experimental developer
tools. Their track record:

- **GitHub Copilot** — born in GitHub Next, graduated to flagship product
- **GitHub Spark** — AI-driven app builder, preview
- **GitHub Blocks** — extensible file viewers, preview
- **gh-aw** — *currently here*: useful and stable enough to use, but APIs and
  behavior may evolve before GA

The honest framing for your audience:

> *"It's a GitHub-built preview tool — production-usable, but with the
> understanding that APIs and behavior may evolve before GA."*

### 1.6 How they relate (one diagram)

```
┌───────────────────────────────────────────────────────────┐
│  GitHub             ← the platform (repos, PRs, users)    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  GitHub Actions  ← the CI engine (YAML, runners)    │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │  gh-aw         ← a Markdown→YAML compiler +   │  │  │
│  │  │                  runtime patterns that target │  │  │
│  │  │                  GitHub Actions               │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                          ↑
        gh CLI talks to all three via the GitHub API
```

**Critical insight:** `gh-aw` is **not a new CI system**. It's a translator that
sits on top of GitHub Actions. Everything you write in `.md` eventually runs as
plain GitHub Actions YAML on plain runners.

### 1.7 The TypeScript analogy

The cleanest way to internalize the relationship:

| TypeScript world | gh-aw world |
|---|---|
| `.ts` file you write | `.md` file you write |
| `tsc` compiler | `gh aw compile` |
| `.js` file the browser runs | `.lock.yml` GitHub Actions runs |
| Node / browser runtime | GitHub Actions runtime |

TypeScript is not a runtime. gh-aw is not a runtime. Both are author-facing
abstractions that compile down to what the underlying runtime understands.

---

## Chapter 2 — What is a "mental model"?

> *Goal: understand the term you're using on Slide 5 so you can explain it if
> someone asks.*

### 2.1 Definition

A **mental model** is the **simplified picture of how something works that you
hold in your head**. It's deliberately less detailed than reality — that's the
point. A good mental model is small enough to fit in working memory but accurate
enough to predict behavior in situations you haven't seen.

### 2.2 Origin of the term

| Year | Who | Contribution |
|---|---|---|
| 1943 | Kenneth Craik (Scottish psychologist) | First wrote that the mind constructs *small-scale models* of reality to anticipate events. |
| 1983 | Philip Johnson-Laird (cognitive scientist) | Popularized in psychology — how humans reason using internal simulations. |
| 1988 | Donald Norman (*The Design of Everyday Things*) | Brought it into design/engineering: how users *think* a system works vs how it *actually* works. |
| 1990 | Peter Senge (*The Fifth Discipline*) | Made it a management/strategy concept. |
| 2010s+ | Engineering culture | "Mental models" became shorthand for transferable thinking patterns. |

### 2.3 Why this term, not "diagram" or "concept"?

| Term | What it implies |
|---|---|
| **Diagram** | A picture, possibly accurate, possibly comprehensive |
| **Concept** | A definition or idea |
| **Mental model** | A *deliberately simplified internal picture* you use to **predict behavior** and **reason about new situations** — and which you *know* is an abstraction |

The phrase carries three useful implications:

1. **Internal** — lives in your head, not on paper. Portable across conversations.
2. **Simplified on purpose** — you've thrown away detail. You accept some
   inaccuracy in exchange for the ability to think fast.
3. **Predictive** — a *good* mental model lets you guess correctly what will
   happen in new scenarios. A *bad* mental model leads to wrong predictions.

### 2.4 Why it matters for your demo

Your own earlier confusion is the perfect illustration. You held this model:

> *"AI converts the `.md` to `.lock.yml`. After that it's just a normal workflow."*

It's plausible. It's almost right. But the wrongness in one specific spot
(AI's role) propagated: you would have predicted "I need an API key for the
compile step" → wrong. You'd have predicted "editing the prompt body needs a
recompile" → also wrong (which is why I myself got it wrong earlier — I built
on your model without correcting it).

Once you replaced it with:

> *"Compile is deterministic; AI runs only at workflow execution time, inside
> one specific job, when a real event fires."*

…every downstream prediction snaps into place.

That's why a presenter spends 90 seconds on the mental model up front instead
of jumping into syntax. Give the audience a correct internal picture and the
rest of the talk lands.

### 2.5 How to use the phrase on stage

> *"A mental model is the simplified picture of a system that fits in your
> head — small enough to be portable, accurate enough to predict behavior.
> The goal of the next slide is to install one in your head."*

That framing tells engineers: *"I respect your time. I'm not teaching you the
manual. I'm giving you the framework so you can read the manual yourself."*
They'll lean in.

---

## Chapter 3 — The three layers

> *Goal: understand the corrected mental model in one diagram and one paragraph.*

### 3.1 The three layers

```
Layer 1: GitHub                  → the platform (where the code lives)
Layer 2: GitHub Actions          → the CI engine (executes YAML)
Layer 3: gh-aw                   → the Markdown→YAML compiler + safe-output runtime
```

Each layer sits on the one below. None of them replaces the one below.

### 3.2 The corrected mental model

```
  ┌──────────────── COMPILE TIME ────────────────┐    ┌─────────────── RUN TIME ───────────────┐
  │                                              │    │                                        │
  │  Where: your laptop                          │    │  Where: a GitHub-hosted runner VM      │
  │  When:  whenever YOU run `gh aw compile`     │    │  When:  whenever a workflow event fires│
  │  Who:   a deterministic Go program (gh-aw)   │    │  Who:   GitHub Actions + Claude API    │
  │  AI?    NO. Zero AI.                         │    │  AI?    YES. Claude is called here.    │
  │  Net?   NO (except to look up action SHAs)   │    │  Net?   YES. Runner calls Anthropic.   │
  │  Key?   NO ANTHROPIC_API_KEY needed          │    │  Key?   YES. Needs ANTHROPIC_API_KEY   │
  │                                              │    │                                        │
  │  Input:  pr-summarizer.md                    │    │  Input: a real PR's diff               │
  │  Output: pr-summarizer.lock.yml              │    │  Output: a comment on the PR           │
  │                                              │    │                                        │
  └──────────────────────────────────────────────┘    └────────────────────────────────────────┘
              ↓ you git commit + push                              ↑ triggered by PR event
              └─────────────────── GitHub repo ────────────────────┘
```

**Compile time** is "build the recipe." **Run time** is "actually cook the
meal." Different kitchens. Different days.

### 3.3 What collapsing the two layers gets you wrong

The single most common error: thinking the AI compiles the file. It doesn't.
The compile step is pure code transformation — like `tsc` for TypeScript or
`go build` for Go. The AI never appears at this stage.

The AI shows up *later*, *inside* the workflow, in one specific job (the
"agent" job), when a real event triggers a run.

---

## Chapter 4 — The two Claudes

> *Goal: stop confusing your IDE-side Claude with the workflow-side Claude.
> They are different processes, on different machines, with different auth.*

### 4.1 The confusion

The word "Claude" appears twice in this project. People assume it's the same
Claude. It isn't.

### 4.2 The clear distinction

| | Claude #1 — in your IDE | Claude #2 — in the workflow |
|---|---|---|
| **Where it runs** | On your laptop, inside Claude Code | On a GitHub Actions runner VM in the cloud |
| **What it does for you** | Helps you write code, docs, slides; runs git/gh; pair-programs | Reads the PR diff and posts the review comment |
| **How it authenticates** | Your personal Claude Code / Anthropic Console login | Reads `ANTHROPIC_API_KEY` from the GitHub repo's secret vault |
| **Needs ANTHROPIC_API_KEY?** | **No** | **Yes — cannot run without it** |
| **When it runs** | Whenever you have a conversation with it | Only when a workflow event fires |
| **Costs whose API budget?** | Your personal / your org's Claude subscription | Whoever owns the key used by the repo |

### 4.3 Why this matters

Three concrete consequences:

1. **You never share your API key with the IDE Claude.** It doesn't need it
   and you should never give it.
2. **Anthropic API billing for the workflow is per-key**, not per-developer.
   Decide carefully: shared org key vs personal key vs per-team keys.
3. **A failed workflow doesn't mean the IDE Claude is broken** (or vice versa).
   Different processes, different failure modes.

### 4.4 Visual

```
Your laptop                          GitHub Actions runner
┌─────────────────────────┐         ┌────────────────────────────┐
│  Claude Code (me)       │         │  Claude (the workflow)     │
│  - auth: your login     │         │  - auth: ANTHROPIC_API_KEY │
│  - reads/writes files   │         │  - reads PR diff           │
│  - runs git/gh commands │         │  - posts PR comment        │
└─────────────────────────┘         └────────────────────────────┘
         │                                       ▲
         │  git push                             │  triggered by PR event
         ▼                                       │
       GitHub repo  ─────────────────────────────┘
```

---

## Chapter 5 — Compile time vs Runtime

> *Goal: internalize the most important distinction in the entire framework.*

### 5.1 The two moments

There are exactly two moments when something interesting happens:

1. **Compile time** — you run `gh aw compile <name>` on your laptop.
2. **Run time** — a GitHub event fires and a runner executes the workflow.

Almost every confusion about gh-aw comes from blending these two together.
Keep them rigidly separated in your head.

### 5.2 Side-by-side table

| Aspect | Compile time | Run time |
|---|---|---|
| **Who triggers it** | You, manually | A GitHub event (PR, push, schedule, comment, etc.) |
| **Where it runs** | Your laptop | A GitHub-hosted runner VM (or self-hosted) |
| **What runs** | The `gh-aw` Go binary | GitHub Actions executor + Claude (via API) |
| **What it reads** | `pr-summarizer.md` | `pr-summarizer.lock.yml` + the live event payload |
| **What it produces** | `pr-summarizer.lock.yml` | A PR comment, an issue, a status, etc. |
| **Deterministic?** | Yes (same input → same output) | No (Claude's output varies) |
| **Internet?** | Mostly no (only to resolve action SHAs) | Yes (calls api.anthropic.com) |
| **`ANTHROPIC_API_KEY` needed?** | **No** | **Yes** |
| **GitHub token needed?** | No | Yes (scoped to the workflow job) |
| **Logs visible?** | Local terminal output | GitHub Actions run UI |
| **How long?** | Sub-second to a few seconds | Typically 30–90 seconds for PR Summarizer |
| **Cost?** | Free | Actions minutes + Claude tokens |

### 5.3 The frequent question: "does compile call Claude?"

**No.** The compile step is a deterministic templating transform. Inputs: the
`.md` and gh-aw's built-in templates. Outputs: the `.lock.yml`. No AI, no API
call (except for SHA lookups on actions). You can run `gh aw compile` offline.

### 5.4 The other frequent question: "does the workflow read the `.md` at runtime?"

**Yes — and this is the subtle part you discovered.** See Chapter 7 for the
proof from your own `.lock.yml`. The lock file contains a `{{#runtime-import
.github/workflows/pr-summarizer.md}}` directive that tells the runner: "fetch
the `.md` from the checked-out repo and use its body as the prompt." So both
files matter at runtime.

---

## Chapter 6 — Anatomy of the `.md` file

> *Goal: understand exactly what's in the file you author, and how each half
> is treated by the compiler.*

### 6.1 The structure

Every `gh-aw` workflow `.md` file has **two parts**, separated by `---`:

```
┌─────── pr-summarizer.md ──────────────────────────────────┐
│ ---                                                       │  ← FRONTMATTER START
│ name: PR Summarizer                                       │
│ on:                                                       │
│   pull_request:                                           │
│     types: [opened, reopened, synchronize, ready_for_review]│  ← (1) FRONTMATTER
│ permissions: { contents: read, pull-requests: read }      │      YAML metadata.
│ engine: claude                                            │      Triggers, perms,
│ tools:                                                    │      tools, safe-outputs.
│   github: { allowed: [get_pull_request_diff, ...] }       │
│ safe-outputs:                                             │
│   add-comment: { max: 1 }                                 │
│ ---                                                       │  ← FRONTMATTER END
│                                                           │
│ # PR Summarizer                                           │  ← (2) BODY
│                                                           │      Plain markdown.
│ You are reviewing a pull request in the gh-aw-demo        │      The prompt Claude
│ repository, a small FastAPI service...                    │      reads at runtime.
│                                                           │
│ ## Your task                                              │
│ 1. Fetch PR metadata, files, diff.                        │
│ 2. Produce ONE markdown comment with:                     │
│    - What changed                                         │
│    - Risk callouts                                        │
│    - ...                                                  │
└───────────────────────────────────────────────────────────┘
```

### 6.2 How compile treats each half

| Half | What `gh aw compile` does | Where it ends up |
|---|---|---|
| **Frontmatter** | Translated, expanded, baked into the YAML structure: `triggers` → `on:` block; `tools` → bash steps with allowlists; `permissions` → `permissions:` block; `safe-outputs` → validator jobs; `engine` → which agent binary to install | **Lives inside `.lock.yml`** as concrete YAML jobs/steps |
| **Body** | **Not touched.** Compile emits a single `{{#runtime-import path/to/file.md}}` directive that points back at the `.md` file. | **Stays in the `.md`.** The lock.yml only references it. |

### 6.3 Consequences of this split

- **Editing the prompt body does NOT require recompile.** Push the change;
  the next workflow run picks it up automatically.
- **Editing the frontmatter REQUIRES recompile.** Otherwise the `.lock.yml`
  is out of sync with your intent and `gh aw verify` will fail.
- **Both files must be committed to the repo.** Runtime needs the lock.yml
  to know how to run, and the .md to know what to ask Claude.

### 6.4 The frontmatter keys, briefly

| Key | Purpose | Example |
|---|---|---|
| `name` | Display name in the Actions UI | `PR Summarizer` |
| `on` | Trigger events | `pull_request: { types: [opened, synchronize] }` |
| `permissions` | The runner's GitHub token scopes | `contents: read, pull-requests: read` |
| `engine` | Which AI engine to use | `claude`, `copilot`, `codex` |
| `tools` | Capability whitelist for the agent | `github: { allowed: [get_pull_request_diff] }` |
| `safe-outputs` | What the agent is allowed to produce | `add-comment: { max: 1 }` |

### 6.5 The body, briefly

The body is **plain markdown** — headings, lists, code blocks, paragraphs.
gh-aw imposes no special template language. Anything you write is, at runtime,
prepended with gh-aw's built-in system prompts and handed to Claude as the
final prompt.

You can also use:

- **Variable interpolation:** `${{ github.event.pull_request.number }}` etc.,
  same as regular Actions YAML.
- **Sub-imports:** `{{#import shared-rules.md}}` to compose prompts from
  smaller markdown files.

---

## Chapter 7 — Anatomy of the `.lock.yml`

> *Goal: understand what's actually in the generated file and why it's 80 KB
> even when the prompt body isn't in it.*

### 7.1 The first three lines (meta-headers)

```yaml
# gh-aw-metadata: {"schema_version":"v3","frontmatter_hash":"...","compiler_version":"v0.74.8",...}
# gh-aw-manifest: {"version":1,"secrets":["ANTHROPIC_API_KEY","GITHUB_TOKEN",...],"actions":[...],...}
# (then ASCII art and a "DO NOT EDIT" banner)
```

These are **JSON comments** gh-aw uses to:

1. Detect tampering (`frontmatter_hash` — if you hand-edit the lock and re-run
   compile, the hash mismatch is detected).
2. Declare what secrets and actions the workflow uses (for security review).
3. Record which compiler version generated the file (so future versions know
   what to expect).

### 7.2 The structural sections

After the metadata comments, the file is a regular **GitHub Actions YAML** with:

| Section | What it contains |
|---|---|
| `name`, `on`, `permissions`, `concurrency`, `run-name` | Top-level workflow metadata (translated from frontmatter) |
| `jobs:` | The 6 jobs that make up the agent runtime |
| Inside each job: `runs-on`, `needs`, `if`, `permissions`, `steps` | Standard Actions YAML, with gh-aw-generated steps |

### 7.3 The 6 jobs (your file's structure)

1. **`pre_activation`** — early metadata pull; decides whether to actually run
2. **`activation`** — sets up the runtime: downloads Claude CLI, prepares the prompt
3. **`agent`** — calls Claude; this is where AI happens
4. **`detection`** — scans Claude's output for safe-output directives
5. **`safe_outputs`** — separate job (with a scoped GitHub token) that executes the validated actions
6. **`conclusion`** — cleanup, status reporting

The split between `agent` (no GitHub token) and `safe_outputs` (scoped token)
is the **core security pattern**. See Chapter 10.

### 7.4 The prompt-builder step (the smoking gun)

Inside the `activation` job, you'll find a step called **"Create prompt with
built-in context"** that uses bash heredocs to build the final prompt. The
key line:

```yaml
cat << 'GH_AW_PROMPT_..._EOF'
</system>
{{#runtime-import .github/workflows/pr-summarizer.md}}
GH_AW_PROMPT_..._EOF
```

That `{{#runtime-import ...}}` is the proof that your prompt body lives in
the `.md`, not in the lock. At runtime, gh-aw's templating engine resolves
that directive by `cat`-ing the `.md` file into the prompt.

### 7.5 Why is the lock still 80 KB if the prompt body isn't in it?

Great question. The lock contains:

- **Pinned action SHAs** — every `uses:` line has the SHA, not a tag.
- **The 6 jobs** — each with its own steps, env vars, conditionals.
- **gh-aw's built-in system prompts** are embedded inline (XPIA defense, MCP
  tool instructions, safe-output guards, GitHub context block — see lines
  214-256 of your file).
- **Validator JavaScript** — the safe-output checks are inline `actions/github-script`
  blocks containing JS that validates Claude's output.
- **Container image pins** — gh-aw uses container images for things like the
  firewall and MCP gateway; each is pinned to a SHA.
- **The `{{#runtime-import}}` directive** is just one line — the rest is all
  infrastructure.

In other words: the lock is mostly the **runtime apparatus** that makes the
agentic workflow safe and reproducible. Your prompt body would add only a few
hundred bytes if it were embedded; the size has nothing to do with it.

---

## Chapter 8 — Why two files?

> *Goal: understand the design rationale so you can defend it in Q&A.*

### 8.1 Reason 1 — Edits to the prompt don't need a recompile

If the prompt body were embedded in the lock, every prompt tweak would
regenerate the lock and produce a large, noisy YAML diff in your PR. Bad
authoring experience.

By keeping the body in `.md` and using runtime-import, prompt edits produce
clean, readable diffs (just the markdown). Only frontmatter changes touch
the lock.

### 8.2 Reason 2 — The lock stays human-readable for security review

A security reviewer's job is to check: *what can this workflow do?* That's
answered by triggers, permissions, secrets, allowed tools, allowed safe-outputs.
All of those live in the lock. Keeping the body out of the lock means the lock
stays ~stable across prompt iterations and focuses the reviewer's attention on
what actually changes the security surface.

### 8.3 Reason 3 — Audit boundary: capability vs intent

Two separate review concerns, two separate files:

| File | Reviews this concern | Who reviews |
|---|---|---|
| `.lock.yml` | **Capability** — what the workflow *can* do (jobs, perms, tools) | Security team, infrastructure team |
| `.md` (body) | **Intent** — what the workflow is *asked* to do (the prompt) | Product team, prompt engineers |

This separation lets non-security-trained engineers iterate on prompts
without re-engaging the security team every time.

### 8.4 Reason 4 — Reproducibility

The lock pins:
- Exact SHAs of every reusable action used
- Exact container image digests for sidecars
- The compiler version that generated it

That means: a workflow that compiled cleanly today will run identically a year
from now, even if every dependency upstream has changed. This is the same
reason `package-lock.json` exists.

### 8.5 The package-lock.json analogy

Strongest single analogy you can use on stage:

| `npm` world | `gh-aw` world |
|---|---|
| `package.json` (you author) | `pr-summarizer.md` (you author) |
| `package-lock.json` (generated) | `pr-summarizer.lock.yml` (generated) |
| Both committed to git | Both committed to git |
| Regenerated by `npm install` | Regenerated by `gh aw compile` |
| Stops surprise dependency changes | Stops surprise workflow-behavior changes |

---

## Chapter 9 — The runtime lifecycle in detail

> *Goal: trace one PR event end-to-end so you can answer "what actually happens?"*

### 9.1 Setup (one-time, before the demo)

1. You've committed both `pr-summarizer.md` and `pr-summarizer.lock.yml` to the repo.
2. You've set `ANTHROPIC_API_KEY` as a repo secret in GitHub's encrypted vault.

### 9.2 The trigger

A teammate opens PR #1 against `main`. GitHub fires a `pull_request` event with
`action: opened`. The event matches the `on:` block in `pr-summarizer.lock.yml`,
so GitHub Actions queues a workflow run.

### 9.3 Runner allocation

GitHub Actions:
- Picks a runner from its pool (Ubuntu, by default)
- Boots a fresh VM
- Installs the Actions executor
- Clones your repo onto the runner (via `actions/checkout`)

The cloned repo includes **both** `pr-summarizer.md` and `pr-summarizer.lock.yml`.

### 9.4 Job 1 — `pre_activation`

Reads the event payload, decides whether the workflow should actually run
(e.g., skip draft PRs, skip if the same workflow is already running on this
ref). If approved, emits `activated=true` and the next job starts.

### 9.5 Job 2 — `activation`

- Installs the Claude Code CLI on the runner
- Builds the prompt by concatenating:
  1. gh-aw's built-in system prompts (XPIA defense, MCP instructions, safe-output rules)
  2. Auto-generated `<github-context>` block (actor, repo, PR number, etc.)
  3. **Your `.md` body** (resolved from the `{{#runtime-import}}` directive)
- Writes the assembled prompt to `/tmp/gh-aw/aw-prompts/prompt.txt`
- Validates the prompt for placeholder injection vulnerabilities
- Logs the prompt for debugging

### 9.6 Job 3 — `agent` (the AI moment)

This is the only job where AI runs.

- Reads `ANTHROPIC_API_KEY` from the GitHub-injected `secrets.*` map
- Opens an HTTPS connection to `api.anthropic.com`
- Sends the prompt + the list of allowed tools + the event payload
- Claude runs, decides which tools to call, calls them via the allowed surface
  (e.g., `get_pull_request_diff` → gh-aw's GitHub MCP server proxy)
- Claude returns a final response that may include safe-output directives
  (e.g., "I want to add this comment: [...]")
- The agent job writes those directives to `/tmp/gh-aw/safeoutputs/outputs.jsonl`
- **Critical:** the agent job's GitHub token is **read-only or unset** for
  anything beyond the explicitly allowed `tools.github` methods. The agent
  cannot push code or create comments directly.

### 9.7 Job 4 — `detection`

Reads `outputs.jsonl` and runs deterministic JavaScript validators against
each entry:
- Is this a recognized safe-output type? (`add-comment`, `create-issue`, etc.)
- Does the workflow's frontmatter actually allow this type?
- Does the entry pass per-type validation (e.g., comment body ≤ N chars,
  no script tags)?

Any failed entry causes the workflow to fail.

### 9.8 Job 5 — `safe_outputs`

This is a **separate job, in a fresh container, with a scoped GitHub token**
that has only the permissions needed to execute the validated outputs (e.g.,
`pull-requests: write` to post a comment).

It reads the validated `outputs.jsonl` and performs the actions one by one
using regular GitHub REST API calls.

The separation matters: even if the agent job was compromised, all it could
do was write entries to a file. The job that has write permissions has no
direct line to Claude.

### 9.9 Job 6 — `conclusion`

Cleanup, summary, optional notifications. The PR now has Claude's comment on it.

### 9.10 Cost & timing

- Wall time: typically 30–90 seconds end-to-end
- Anthropic token cost for a 500-line PR: single-digit cents
- GitHub Actions minutes: small (≤ 1 minute on Ubuntu = cheapest tier)

---

## Chapter 10 — The security model

> *Goal: understand gh-aw's defense-in-depth layers so you can answer the
> "what about prompt injection?" question with confidence.*

### 10.1 The threat model

What could an attacker do to abuse an agentic workflow?

1. Plant malicious instructions in PR content (title, body, diff comments, file
   contents) hoping the agent will execute them. This is **prompt injection**.
2. Swap out a referenced GitHub Action tag (`actions/foo@v1`) for malicious code
   pushed under the same tag. This is a **supply-chain attack**.
3. Sneak in a new secret reference hoping nobody notices. This is a **secret
   exfiltration attempt** via the workflow surface.
4. Tamper with the lock file directly to bypass the safe-output sandbox.

### 10.2 The four defenses

| Defense | What it protects against | How it works |
|---|---|---|
| **Capability whitelist** (`tools:` block) | Agent calling unauthorized APIs | Agent can literally only call methods listed in `tools.github.allowed` |
| **Safe-outputs sandbox** | Agent making unauthorized changes | Agent writes *intent* to a file; a separate validator job executes only whitelisted outputs |
| **Action SHA pinning** (`.github/aw/actions-lock.json`) | Tag-swap supply-chain attacks | Every action `uses:` is pinned to a SHA, not a tag |
| **Safe-update mode** (the warning you saw) | Silent introduction of new secrets/actions | Compiler refuses to silently approve new secret/action references; requires `--approve` |

### 10.3 The hands-vs-brain pattern (the most important one)

The single most distinctive design choice in gh-aw:

> **The job with the brain has no hands. The job with the hands has no brain.**

- The `agent` job (has Claude) has no GitHub write token. It can think and
  propose actions, but cannot execute them.
- The `safe_outputs` job (has a scoped GitHub token) cannot call Claude. It
  can only execute pre-validated actions.

Result: even a perfectly successful prompt-injection attack can only convince
Claude to *want to do* something bad. That want has to pass through the
validator. The validator is deterministic JavaScript. It does not get fooled
by clever language.

### 10.4 The `--approve` flow (what you saw)

When gh-aw detects a new restricted reference (a new secret, a new action,
a redirect URL change), it refuses to silently produce the lock. It outputs a
"safe update mode" warning and asks for `--approve`.

`--approve` writes a hash of the approved references into the lock as a marker.
On subsequent compiles:
- If references haven't changed → no warning, no `--approve` needed
- If a new reference appears → warning fires again

This forces a human eyeball on every security-surface change. It's not a strong
cryptographic guarantee, but it's a strong process-level guardrail.

### 10.5 The `actions-lock.json` file

Lives at `.github/aw/actions-lock.json`. Contains:

```json
{
  "entries": {
    "actions/github-script@v9.0.0": {
      "repo": "actions/github-script",
      "version": "v9.0.0",
      "sha": "3a2844b7e9c422d3c10d287c895573f7108da1b3"
    }
  }
}
```

Every action used by any gh-aw-generated lock file is recorded here with its
exact SHA. If `actions/github-script@v9.0.0` ever points to a different SHA in
the future (because the tag was force-moved or compromised), gh-aw refuses to
silently use the new SHA.

### 10.6 What gh-aw does NOT protect against

Be honest with your audience:

- **Cost-of-tokens runaway** — a malicious PR could try to exhaust your
  Anthropic credit by inflating the diff. (Mitigation: token limits per run,
  per-repo budget alarms.)
- **Agent quality** — a poorly written prompt produces poor reviews. The
  safety model protects the *system*, not the *quality of output*.
- **Anthropic outage** — if api.anthropic.com is down, the workflow fails.
  PR review continues normally via humans.
- **Data sent to Anthropic** — your prompt + PR diff is sent over HTTPS to
  Anthropic's API. Anthropic's enterprise terms cover handling; for
  RealPage-specific compliance, route through your security/privacy team.

---

## Chapter 11 — The cast of characters

> *Goal: a quick reference for who's responsible for what.*

| Role | Identity | When active | What it does |
|---|---|---|---|
| **You** | The developer | Always | Author `.md`, run `gh aw compile`, `git push` |
| **`gh aw` CLI** | Go binary on your machine | Compile time | Reads `.md` frontmatter, expands templates, emits `.lock.yml`. **Pure code transformation. No AI.** |
| **`git` / GitHub.com** | Source-control service | When you push, when events fire | Stores the repo, fires events when PRs open, etc. |
| **GitHub Actions** | The CI engine | Runtime | Sees the event, reads `.lock.yml`, allocates a runner, executes the YAML's jobs in order |
| **The runner** | An Ubuntu VM (or Windows, or self-hosted) | Runtime | The actual computer running each job. Has its own filesystem; can make HTTPS calls. |
| **The "agent job"** | One specific job in the lock | Mid-run | Calls Claude's API. The only place AI runs. |
| **Anthropic** | The company that makes Claude | While processing API calls | Receives the prompt + diff over HTTPS; returns Claude's response |
| **Claude** | The AI model | While processing API calls | Reads the diff, decides which tools to call, writes the response text |
| **`ANTHROPIC_API_KEY`** | Encrypted secret string (`sk-ant-...`) | Used only by the agent job | Authenticates the runner to Anthropic. Without it, Anthropic refuses. |
| **`GITHUB_TOKEN`** | Auto-injected token | Used by the runner | Lets the runner call GitHub's API (scoped per workflow's `permissions:`) |

---

## Chapter 12 — Terminology cheat-sheet

> *Use this as a glossary you can flash open during Q&A.*

| Term | Meaning |
|---|---|
| **GitHub** | The platform/website that hosts your repos. |
| **GitHub Actions** | The CI/CD engine built into GitHub. Runs YAML pipelines on runners. |
| **Workflow** | A YAML file in `.github/workflows/` that GitHub Actions executes when its `on:` events fire. |
| **Runner** | The VM (or self-hosted machine) on which a workflow's jobs execute. |
| **`gh`** | GitHub's official CLI tool. |
| **`gh aw`** | GitHub Agentic Workflows. A `gh` extension built by GitHub Next that adds Markdown-authored workflows. |
| **GitHub Next** | GitHub's experimental engineering lab. Origin of Copilot, Spark, Blocks, and gh-aw. |
| **`.md` (workflow source)** | The Markdown file you author. Two parts: frontmatter + body. |
| **`.lock.yml`** | The generated YAML GitHub Actions actually executes. Compiled from `.md` by `gh aw compile`. |
| **Frontmatter** | The YAML block at the top of the `.md`, between `---` markers. Holds triggers, permissions, tools, safe-outputs, engine. |
| **Body** | The Markdown content of the `.md` after the frontmatter. The English prompt Claude reads at runtime. |
| **Runtime-import** | A template directive (`{{#runtime-import path}}`) in the lock that tells the runner to read a file at execution time. How the lock references the `.md` body. |
| **Agent** | An LLM (Claude, Copilot, Codex) that can call tools and make decisions, not just generate text. |
| **LLM** | Large Language Model. The AI underneath an agent. Claude is an LLM. |
| **Tool** | A capability the agent can call: a GitHub API method, a bash command, an MCP server endpoint. |
| **MCP** | Model Context Protocol. Anthropic's open standard for exposing external tools to an agent. |
| **Safe-output** | A whitelisted action the agent is allowed to *propose* (`add-comment`, `create-issue`, etc.). A separate validated job executes it. |
| **Sandbox** | A constrained execution environment that limits what an isolated piece of code can do. The agent job is sandboxed. |
| **Prompt injection** | An attack where adversarial instructions are embedded in user-controlled content (PR body, file content) in the hope the agent will obey. |
| **`actions-lock.json`** | gh-aw's file at `.github/aw/actions-lock.json` that pins every referenced action to a specific SHA. |
| **Safe-update mode** | gh-aw compiler mode that refuses to silently produce a lock when new secrets/actions appear; requires explicit `--approve`. |
| **`gh aw compile`** | The command that translates `.md` → `.lock.yml`. Local, deterministic, no AI. |
| **`gh aw init`** | One-time scaffolding command: creates `.github/workflows/`, `.github/aw/actions-lock.json`. Does NOT create any workflow. |
| **`gh aw add`** | Pulls a workflow template from gh-aw's built-in catalog. |
| **`gh aw trial`** | Runs a workflow against a *clone* of someone else's repo without touching the original. |
| **Anthropic** | The company that makes Claude (the AI model). |
| **Claude** | Anthropic's AI model family. Multiple sizes (Opus, Sonnet, Haiku). |
| **`ANTHROPIC_API_KEY`** | The secret credential that lets your code call Anthropic's API. Starts with `sk-ant-`. |
| **`GITHUB_TOKEN`** | GitHub Actions auto-injects this token per job, scoped by the workflow's `permissions:` block. |
| **Engine** | The `engine:` frontmatter key. Determines which AI provider gets called (`claude`, `copilot`, `codex`). |
| **Mental model** | A deliberately simplified internal picture of how a system works. Small enough to fit in your head, accurate enough to predict behavior. |

---

## Chapter 13 — Common misconceptions and corrections

> *These are the wrong models people (including me, earlier in our chat)
> initially hold. Pre-rehearse the corrections.*

### Misconception 1: "AI converts the `.md` to `.lock.yml`."

**Correction.** The compile step is a deterministic Go program (`gh aw`). No
AI is involved, no network calls beyond SHA lookups. The AI shows up only at
runtime, inside the `agent` job.

### Misconception 2: "Once compiled, the workflow is just normal YAML — gh-aw is out of the picture."

**Half right.** The lock IS standard GitHub Actions YAML. But at runtime, the
lock contains template directives (`{{#runtime-import ...}}`) and references to
gh-aw's runtime infrastructure (the `gh-aw-actions/setup` action, gh-aw-firewall
containers, etc.). So gh-aw participates in execution, even though the
*orchestration layer* is plain Actions.

### Misconception 3: "I need to recompile every time I edit the `.md`."

**Mostly wrong.** You need to recompile only when you change the **frontmatter**
(triggers, tools, permissions, safe-outputs, engine). Edits to the prompt body
are picked up automatically via `{{#runtime-import}}`. (I initially told you
"recompile every change" — that was an oversimplification.)

### Misconception 4: "`ANTHROPIC_API_KEY` is needed for compile."

**Wrong.** Compile is offline-friendly. The key is needed only at runtime, by
the runner, when the agent job calls Anthropic.

### Misconception 5: "Anthropic key = Claude."

**Almost right.** Anthropic is the company. Claude is one of Anthropic's
products. `ANTHROPIC_API_KEY` is the credential that lets your code call
Anthropic's API, which then runs Claude on your behalf. Practically, "the
Anthropic key" = "the key that lets the workflow talk to Claude." Conceptually,
remember it's a credential, not the AI itself.

### Misconception 6: "The agent can push code to my repo."

**Wrong by design.** The agent job has no write permissions. Any change that
affects the repo must go through `safe-outputs` (e.g., `create-pull-request`),
which is executed by a separate, validated job. Even then, the agent can only
*open* a PR — humans still merge.

### Misconception 7: "Claude in my IDE and Claude in the workflow are the same Claude."

**Wrong.** Two separate processes, on different machines, with different
authentication. See Chapter 4.

### Misconception 8: "gh-aw is a brand-new CI system."

**Wrong.** It's a compilation layer on top of standard GitHub Actions. No new
infrastructure, no new agents, no new runners.

### Misconception 9: "gh aw init creates my workflows."

**Wrong.** `gh aw init` only sets up the folder structure and the
`actions-lock.json`. To create a workflow you either `gh aw add <template>`
or hand-write the `.md`.

### Misconception 10: "The .lock.yml is huge because the prompt is in it."

**Wrong.** The prompt body lives in the `.md`, not the lock. The lock is
80 KB because it contains the 6 jobs, action SHA pins, container image
digests, safe-output validators (JavaScript), and gh-aw's built-in system
prompts that get prepended to your prompt at runtime.

---

## Chapter 14 — The practical workflow-author lifecycle

> *Goal: the daily flow once you're past the first run.*

### 14.1 Day one (first time setup, per repo)

1. `gh aw init` — creates `.github/aw/actions-lock.json` and `.gitattributes`.
2. `gh aw add <template>` OR hand-write `pr-summarizer.md`.
3. `gh aw compile pr-summarizer --approve` — generates the lock; `--approve`
   confirms the secret/action references.
4. Set `ANTHROPIC_API_KEY` as a repo secret.
5. `git add . && git commit && git push`.
6. Open a test PR. Watch the workflow run.

### 14.2 Day two onwards (typical edits)

| You want to... | Do this |
|---|---|
| Tweak the prompt wording | Edit `.md` body. Push. No recompile needed. |
| Add a new safe-output type | Edit `.md` frontmatter. Run `gh aw compile`. If it warns, `--approve`. Push. |
| Add a new allowed tool | Edit `.md` frontmatter. Run `gh aw compile`. Push. |
| Change triggers (e.g., add `issues:`) | Edit `.md` frontmatter. Run `gh aw compile`. Push. |
| Switch from Claude to Copilot | Change `engine: claude` to `engine: copilot`. Recompile. Push. |
| Bump pinned action SHAs | Run `gh aw compile --update-actions` (verify the exact flag in CLI help). Push. |
| Verify your lock matches your `.md` | Run `gh aw verify`. Useful as a CI gate. |
| Test against a real repo without modifying it | `gh aw trial <workflow> <target-repo>`. |

### 14.3 Useful CI step

Add a CI check on every PR that runs `gh aw verify`. This fails the build if
someone edits the `.md` without running `gh aw compile`. Prevents drift.

### 14.4 Cost discipline

- Anthropic API is billed per token. Estimate your monthly usage before
  rolling out org-wide.
- Use `vars.GH_AW_MODEL_AGENT_CLAUDE` to pin a specific model (e.g.,
  `claude-haiku-4-5` for cheaper runs, `claude-opus-4-6` for higher quality).
- GitHub Actions minutes are billed per runner-minute. Most agent runs are
  well under a minute.

---

## Chapter 15 — Things you will inevitably forget

> *Quick-hit warnings worth re-reading the morning of the demo.*

- The `engine:` key is at the **top level** of frontmatter, not nested under `tools:`.
- `safe-outputs.add-comment.max` defaults to 1 — be explicit anyway.
- `gh aw compile` is silent on success. Re-run with `--verbose` if you suspect nothing happened.
- The agent job's logs don't show Claude's full chain-of-thought — only the final tool calls. To debug prompts, use `gh aw trial` locally first.
- If `.lock.yml` doesn't update after compile, you're probably in the wrong directory. The CLI is `cwd`-sensitive.
- `--approve` is sticky: once embedded in the lock, future identical-reference compiles don't re-warn.
- Prompt body edits don't bump the `frontmatter_hash` in the lock — that's by design.
- `.claude/settings.local.json` is per-developer, NOT a project file. Always gitignored.
- `.gitattributes` (created by gh-aw) marks `*.lock.yml` as `linguist-generated` so GitHub collapses them in PR diffs. Keep it committed.
- Self-hosted runners work identically — set `runs-on: self-hosted` in frontmatter.
- The "two Claudes" trap: the Claude helping you author (in Claude Code) is NOT the Claude that will run in your workflow.

---

## Appendix A — Pre-demo checklist

Run through Wednesday night, in this order.

- [ ] `gh-aw-demo` repo exists on GitHub, code pushed, lock.yml present, `--approve` applied
- [ ] `ANTHROPIC_API_KEY` set as a repo secret on `gh-aw-demo`
- [ ] One test PR is open with Claude's comment visible (for fallback if live demo fails)
- [ ] Screenshots in `presentation/assets/` are up to date (and reflect the NEW repo, not the trial repo if possible)
- [ ] Browser bookmark to `file:///.../presentation/index.html` set
- [ ] Browser zoomed to a comfortable level for the projector resolution
- [ ] Speaker notes work (press `.`)
- [ ] Overview grid works (press `Esc`)
- [ ] Backup PDF export of the deck on USB stick
- [ ] One-paragraph elevator pitch memorized for the "what is this?" hallway question
- [ ] Re-read Chapter 13 (Misconceptions) the morning of the demo

---

## Appendix B — FAQ to rehearse before Q&A

| Question | Crisp answer |
|---|---|
| *"How much does it cost?"* | Anthropic API charges per token; PR Summarizer on a typical diff = single-digit cents. Billing rolls up to whoever owns the API key. |
| *"Can we use Copilot instead of Claude?"* | Yes. Change `engine: claude` to `engine: copilot`. Uses your existing Copilot Enterprise entitlement — no separate billing. |
| *"What if the agent goes rogue?"* | Two layers: agent job has no repo-writing permissions; safe-outputs validator inspects every proposed action. The brain has no hands. |
| *"Can it modify code?"* | Only via `safe-outputs.create-pull-request`. Even then, it opens a PR — a human still merges. There's no "agent pushes to main" mode. |
| *"Self-hosted runners?"* | Yes, same as any GitHub Action. `runs-on: self-hosted` in frontmatter. |
| *"Data privacy / where does our code go?"* | Diff + prompt are sent over HTTPS to Anthropic. Anthropic's enterprise terms cover handling. For RealPage compliance specifics, route to the security team. |
| *"Can I write my own workflow?"* | Yes — that's the workshop. The `.md` is just markdown with frontmatter. |
| *"Will this replace human code review?"* | No. It removes the boring 80% so reviewers focus on the 20%. The agent is a triager, not a gatekeeper. |
| *"What if Anthropic is down?"* | The workflow fails on that run. PR review continues normally. Re-run when Anthropic recovers. |
| *"Is gh-aw GA?"* | Public preview. Production-usable but APIs may evolve. Built by GitHub Next, the same lab that built Copilot. |
| *"Why two files (`.md` and `.lock.yml`)?"* | Same reason as `package.json` + `package-lock.json`. One you author, one is generated. Lock is checked in for reproducibility and security review. |
| *"Does compiling call Claude?"* | No. Compile is a deterministic local transform. No AI, no network calls (except SHA lookups). |
| *"Do I need to recompile when I tweak the prompt?"* | No — body edits are picked up automatically via `{{#runtime-import}}`. Recompile only when you change frontmatter. |

---

## Appendix C — Further reading & references

- **Official gh-aw repo:** `github.com/githubnext/gh-aw`
- **GitHub CLI:** `cli.github.com` and `github.com/cli/cli`
- **GitHub Next:** `githubnext.com`
- **Anthropic — "Building Effective Agents":** Anthropic's reference essay on what
  constitutes an agent vs a simple LLM call. Worth reading before defining
  "agent" in your talk.
- **Model Context Protocol (MCP):** `modelcontextprotocol.io` — Anthropic's
  open standard for tool exposure.
- **GitHub Actions docs:** `docs.github.com/en/actions` — the underlying CI
  layer everything runs on.
- **Donald Norman — *The Design of Everyday Things*:** the source for the
  modern engineering use of "mental model."
- **Your own companion docs:** `C:\Practice\AI\GithubAgenticWorkflow\docs\`
  (1-introduction.md through 4-case-study-pr-summarizer.md).

> Always verify URLs before citing them live on stage — paths in the
> githubnext org sometimes move.

---

*End of deep-dive. Update as you learn more.*
