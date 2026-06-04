# GitHub Agentic Workflows — Presentation Script

> **Companion to** `index.html` — speaker notes for the 30-minute introduction.
> One section per slide: what's on the slide + what to say (~30–60 seconds of
> spoken script, ~120 words). Read at a normal pace and you'll land at 30 min.

---

## How to use this document

- Each `## Slide N — <title>` section corresponds to one slide in `index.html`.
- **On screen** describes what the audience sees.
- **What to say** is your spoken script — read it almost verbatim the first
  time, then make it your own.
- **Transition** is a one-line hook into the next slide so you don't pause
  awkwardly.
- The time at the top of each section is the **cumulative** elapsed time when
  you finish that slide.

---

## Slide 1 — Title  (0:00–0:00)

**On screen:** Title — "GitHub Agentic Workflows. Automation you write in English, not YAML." Your name and date.

**What to say:**
> Good morning. Today we're spending 30 minutes on **GitHub Agentic Workflows**
> — also called **gh-aw**. This is GitHub's official take on combining
> CI/CD with AI agents. By the end of this session you'll have a working
> mental model of what these workflows are, how the pieces fit together, and
> you'll have seen two real workflows running end-to-end. This is an
> awareness session, not a workshop — hands-on sessions follow. So sit back,
> ask questions any time, and let's get started.

**Transition:** *"Let me start with where this is coming from."*

---

## Slide 2 — The shift that's coming  (0:00–0:02)

**On screen:** A three-line progression — 2010s wrote code, 2020s wrote YAML, now we write English. Subtitle: "gh-aw is GitHub's official answer."

**What to say:**
> Think about how automation has evolved. In the **2010s** we wrote code,
> and CI/CD ran it. In the **2020s** we wrote **YAML pipelines** to
> orchestrate that code — most of you have lived through this with TFS or
> Azure DevOps. **Now**, in 2026, we're writing **intent in plain English** —
> and AI agents figure out the steps at runtime. GitHub Agentic Workflows
> is GitHub's official answer to this shift. It's not a side project — it's
> built by GitHub Next, the same lab that built Copilot.

**Transition:** *"So what exactly IS an agentic workflow?"*

---

## Slide 3 — What is an agentic workflow?  (0:02–0:04)

**On screen:** One-line definition — "a regular GitHub workflow where instead of writing commands, you write an English prompt that an AI agent executes." Three cards: Triggered by / Run by / Constrained by. Three example workflow ideas at the bottom.

**What to say:**
> An agentic workflow **is** a GitHub workflow — same family as the YAML files
> you already know. It's **triggered** by the same events: a PR opens, a
> schedule fires, an issue is created. It runs on the **same runners**.
> The one new ingredient is that instead of writing the steps yourself,
> you write a **prompt in English** and an **AI agent** — Claude, Copilot,
> or Codex — figures out what to do at runtime. And critically, it's
> **constrained** — the agent can only use tools you allow-listed and can
> only produce outputs you explicitly permit. Examples on screen: review
> every PR, summarize yesterday's test failures, auto-label PRs.

**Transition:** *"Let me show you how that differs from a plain workflow."*

---

## Slide 4 — Plain YAML vs Agentic .md  (0:04–0:05)

**On screen:** Two-column comparison. Plain workflow on left (you write every step, ~200 lines). Agentic workflow on right (you write the goal, ~25 lines).

**What to say:**
> Side-by-side. A **plain YAML workflow** — you write every step explicitly,
> hard-coded commands, shell scripts. Predictable, deterministic, and
> typically a couple hundred lines for any non-trivial task. An **agentic
> workflow** — you write the **goal in plain English**, allow-list a few
> tools, and the agent picks the steps. About **twenty-five lines** for
> the same task. Both files live in `.github/workflows/`. Both run on the
> same runners. Both respect the same security boundaries. The only
> difference is **who decides the steps** — you, or the agent.

**Transition:** *"Now let me give you the one diagram you need to keep in your head."*

---

## Slide 5 — The one diagram  (0:05–0:07)

**On screen:** Three-box flow diagram. "YOU write workflow.md" → "gh aw compile generates" → "GitHub Actions runs workflow.lock.yml."

**What to say:**
> This is the one diagram that unlocks everything. **You** write a file
> called `workflow.md`. You run **`gh aw compile`** — that's a Go program,
> deterministic, no AI involved. It generates a second file:
> `workflow.lock.yml`. **GitHub Actions** then runs that lock file like any
> other pipeline — and somewhere in the middle, it calls Claude. If you
> remember nothing else from this talk: `.md` is what you write, `.lock.yml`
> is what runs. Author intent on the left, machinery on the right.

**Transition:** *"Now there's a confusion that trips everyone up — let me get it out of the way."*

---

## Slide 6 — The two Claudes  (0:07–0:08)

**On screen:** Two cards side by side. Left: "Author-time Claude (Claude Code)" — your IDE, helps you write the .md, loads .claude/ subagents. Right: "Runtime Claude (gh-aw agent)" — sandboxed runner, executes the workflow, uses ANTHROPIC_API_KEY.

**What to say:**
> The single most common source of confusion: there are **two completely
> different Claudes** involved here. On the left, the **author-time
> Claude** — that's Claude Code, the IDE assistant that helps you *write*
> the workflow file. It loads your `.claude/` config and subagents.
> It **never runs in CI**. On the right, the **runtime Claude** — a
> different process entirely. It runs in a sandboxed GitHub runner when
> the workflow fires. It uses your repo's `ANTHROPIC_API_KEY` secret. It
> only sees what your `.md` file explicitly exposes. **Different processes,
> different contexts, different jobs.** Keep them separate in your head.

**Transition:** *"With those two Claudes in mind, here are the moving parts you'll actually touch."*

---

## Slide 7 — Two files, three commands  (0:08–0:09)

**On screen:** Two cards. Left card lists the two files (.md and .lock.yml). Right card shows the three commands: `gh aw init`, `gh aw add`, `gh aw compile`.

**What to say:**
> Two files: the **`.md`** you author, the **`.lock.yml`** that's generated.
> Three commands that cover ninety-five percent of usage. **`gh aw init`** —
> one time per repo, sets up scaffolding. **`gh aw add`** — pulls in a
> workflow template from the catalog. **`gh aw compile`** — every time you
> change the frontmatter of your `.md`. Then it's just normal git: add,
> commit, push. Think of it like `package.json` plus `package-lock.json` —
> you author one, the tool maintains the other.

**Transition:** *"Now let's open up that .md file and look at what's actually in it."*

---

## Slide 8 — Anatomy: overall .md structure  (0:09–0:10)

**On screen:** A full, annotated `.md` file. Top half labelled "frontmatter starts/ends" between `---` markers. Bottom half labelled "body starts (the prompt)".

**What to say:**
> Here's a complete agentic workflow on one screen. Two parts separated by
> `---` markers. The top half is **frontmatter** — YAML configuration:
> when it runs, what engine, what permissions, what tools, what outputs
> are allowed. The bottom half is the **body** — plain markdown, in
> English. That's the prompt the agent reads. The whole file fits on a
> single screen. Compare that to the lock file it compiles to: that's
> over a thousand lines. You don't write that, you don't read it, you
> don't debug it.

**Transition:** *"Let me walk you through what each frontmatter field actually does."*

---

## Slide 9 — Anatomy: frontmatter fields  (0:10–0:12)

**On screen:** Table with three columns — Field, What it controls, Required? Rows: on, engine, permissions, tools, safe-outputs, imports.

**What to say:**
> Six frontmatter fields you'll see in almost every workflow. **`on:`** —
> when does it run; the same trigger syntax as any GitHub workflow.
> **`engine:`** — which AI does the work; `claude`, `copilot`, or `codex`.
> **`permissions:`** — what GitHub scopes the run gets; lock these down.
> **`tools:`** — what the agent is *allowed to call* — for example the
> GitHub MCP server, or bash, or web fetch. **`safe-outputs:`** — what
> the agent is *allowed to produce* — comments, issues, PRs, labels.
> And the optional **`imports:`** — pull in shared markdown content,
> for example from your `.claude/` directory. We'll come back to that
> one in Demo 2.

**Transition:** *"And the body — that's the prompt itself."*

---

## Slide 10 — Anatomy: the body (your prompt)  (0:12–0:13)

**On screen:** A markdown body for the PR Summarizer — a header, instructions, a numbered list of sections. Bullet points below summarize key properties.

**What to say:**
> The body is just markdown. No magic. This is **exactly what Claude sees**
> at runtime, alongside the PR diff that's fetched via the tools you
> allow-listed. **Be specific.** Name the output format. Set hard limits.
> Tell the agent what NOT to do. The clearer the prompt, the better the
> output. And one nice property — **body edits don't require recompile**.
> Change the prompt, commit, push, done. The frontmatter contract is what
> gets baked into the lock file; the body is loaded fresh on every run.

**Transition:** *"OK — you've written the file. What actually happens when it runs?"*

---

## Slide 11 — What runs, step by step  (0:13–0:14)

**On screen:** Vertical flow of six labelled boxes — event fires, runner starts, activation, agent, safe_outputs, conclusion.

**What to say:**
> Six sequential jobs. **One** — an event fires, like a PR being opened.
> **Two** — GitHub Actions reads the lock file and starts a runner.
> **Three** — the `activation` job pulls in your prompt and sets up Claude.
> **Four** — the `agent` job is where the real work happens; Claude reads
> the diff via allowed tools, decides what to say. **Five** — `safe_outputs`
> validates what the agent wants to do and executes only what you
> allow-listed. **Six** — `conclusion` finalizes the run. You don't need
> to memorize this — but you'll see these six boxes in the Actions UI,
> and when something fails the job name tells you where to look.

**Transition:** *"That fifth job — safe_outputs — is where the security story lives."*

---

## Slide 12 — Why safe-outputs change everything  (0:14–0:15)

**On screen:** Two-column comparison. Left (red): "Without safe-outputs" — agent has a token, can do anything. Right (green): "With safe-outputs" — sandboxed, writes intent to a file, separate job validates.

**What to say:**
> This is the security pitch. **Without safe-outputs**, the agent has a
> GitHub token and can do anything that token allows — push to main,
> delete branches, leak secrets. **With safe-outputs**, the agent runs in
> a sandboxed job with **no write token**. It writes its intent to a file
> — "post this comment" — and a **completely separate job** validates and
> executes only the actions you allow-listed. The agent has a brain but
> no hands. Translation: even a **prompt-injection attack** can't make
> the agent push code. This is why gh-aw is production-safe versus just
> handing Claude an API token and hoping.

**Transition:** *"OK, you understand the model. Now let's talk about actually creating one."*

---

## Slide 13 — The 9-step loop  (0:15–0:16)

**On screen:** Three cards — Setup (steps 1–3), Author (steps 4–6), Ship & iterate (steps 7–9).

**What to say:**
> Here's the **end-to-end loop** for creating an agentic workflow. **Setup**
> happens once: install the extension, run `gh aw init` in your repo,
> set your API key as a repo secret. **Authoring** is repeated for each
> workflow: write the `.md`, run `gh aw compile`, commit both files.
> **Ship and iterate**: push to the default branch, trigger the workflow,
> watch the logs, refine your prompt. This same nine-step loop applies
> to every workflow you'll ever build. If all your prerequisites are met,
> you can have your first one running in about ten minutes.

**Transition:** *"Let me show you the actual commands for each step."*

---

## Slide 14 — Steps 1–4: set up & author  (0:16–0:17)

**On screen:** A code block with four numbered commands — install extension, `gh aw init`, `gh secret set`, `gh aw add` or hand-write.

**What to say:**
> Steps one through four — set up and author. **One**: install the
> extension. One-time, per machine. **Two**: `gh aw init` inside the repo
> you want to use. This creates the scaffolding. **Three**: set your
> Anthropic API key as a repo secret. You can do this via the GitHub UI
> or `gh secret set`. **Four**: author the workflow file. The fastest
> path is `gh aw add` with a template name — pulls in a maintained
> template from the gh-aw catalog. The longer path is to hand-write the
> `.md` yourself, using the anatomy slides as a guide.

**Transition:** *"Once you've authored it, here's what shipping looks like."*

---

## Slide 15 — Steps 5–9: compile, ship, iterate  (0:17–0:19)

**On screen:** A code block with the remaining five steps — `gh aw compile`, `git add` (both files), `git commit`, `git push`, `gh pr create`, `gh run watch`.

**What to say:**
> Steps five through nine — compile, ship, iterate. **Five**: `gh aw
> compile` turns your `.md` into a `.lock.yml`. Deterministic, no AI
> involved — it's a Go program. **Six**: critically, commit **both files
> together**. The most common day-one mistake is forgetting the lock
> file. **Seven**: push to the default branch — the workflow
> auto-registers, no separate step. **Eight**: trigger it by opening any
> PR. **Nine**: `gh run watch` follows the run in real time. To change
> the prompt later, just edit the `.md` body and push — no recompile
> needed for body-only edits.

**Transition:** *"OK — enough theory. Let me show you a real one running."*

---

## Slide 16 — Demo 1 intro: PR Summarizer  (0:19–0:20)

**On screen:** Demo intro slide. Three cards — Input (any PR), Agent (Claude), Output (one markdown comment). Source repo URL at the bottom.

**What to say:**
> **Demo one — the PR Summarizer.** This is the canonical first workflow
> for any team. It fires when a PR opens. Claude reads the diff,
> classifies risk, checks test coverage, and posts **one structured review
> comment** — typically within sixty seconds. Read-only GitHub access,
> single comment as output, low blast radius. I'm going to walk you
> through five screenshots from a real run on our demo repo.

**Transition:** *"Step one — a developer opens a PR."*

### Authoring prompt (if asked "what did you tell Claude to write this?")

> *Paste this into Claude Code in the IDE, in the `gh-aw-demo` repo:*
>
> ```
> Create a new GitHub Agentic Workflow at .github/workflows/pr-summarizer.md
> for this FastAPI Mini Notes repo. It should trigger on every PR
> (opened / reopened / synchronize / ready_for_review) plus workflow_dispatch
> with a pr_number input for manual testing.
>
> Engine: claude. Permissions: contents:read + pull-requests:read only.
> Tools: github MCP allow-list = get_pull_request, get_pull_request_files,
> get_pull_request_diff, list_commits, get_file_contents. Plus bash.
>
> Safe outputs: exactly one add-comment, max: 1.
>
> The body prompt should instruct Claude to post ONE structured review
> comment with these sections: What changed, Files touched, Risk callouts
> (🔴/🟡/🟢 with explicit rules for app/store.py changes, new endpoints,
> tests-only), Test coverage, Suggested next steps. Cap at ~400 words.
> Start the comment with "## 🤖 PR Summary".
>
> Then run gh aw compile and commit both pr-summarizer.md and
> pr-summarizer.lock.yml.
> ```

---

## Slide 17 — Demo 1 / Step 1 — PR opened  (0:20–0:20)

**On screen:** Screenshot of a PR being opened on GitHub.

**What to say:**
> Nothing unusual on this screen. Developer opens a normal pull request,
> just like any other day. Zero agent-specific UI here. That's the
> point — the agent is **invisible until it's useful**.

**Transition:** *"Within seconds, the workflow triggers."*

---

## Slide 18 — Demo 1 / Step 2 — workflow triggered  (0:20–0:21)

**On screen:** Screenshot of the Checks tab showing "PR Summarizer" queued/running.

**What to say:**
> The Checks tab shows the PR Summarizer queued and starting to run. This
> is the **same surface** as any other GitHub Actions workflow — same
> Actions tab, same logs, same retry buttons. **Nothing new to learn
> operationally.** That's a big win for adoption.

**Transition:** *"Open the run and you'll see the 6 jobs we discussed."*

---

## Slide 19 — Demo 1 / Step 3 — 6 jobs executing  (0:21–0:22)

**On screen:** Screenshot of the workflow run showing the six sequential jobs.

**What to say:**
> Inside the run, the **six jobs** we covered earlier:
> `pre_activation` → `activation` → `agent` → `detection` → `safe_outputs`
> → `conclusion`. Each is a separate sandboxed step. The `agent` job
> in the middle is where Claude actually thinks. The `safe_outputs` job
> is where the comment actually gets posted.

**Transition:** *"In under a minute, it's done."*

---

## Slide 20 — Demo 1 / Step 4 — completed  (0:22–0:23)

**On screen:** Screenshot showing all six jobs green and complete.

**What to say:**
> All six jobs green. **Typical runtime: thirty to ninety seconds.**
> **Cost per run: pennies** of Anthropic API spend, plus a fraction of
> a runner-minute. And this happens on **every single PR**, automatically,
> with no human in the loop until the comment appears.

**Transition:** *"And here's the comment Claude posts."*

---

## Slide 21 — Demo 1 / Step 5 — Claude's comment  (0:23–0:24)

**On screen:** Screenshot of the bot's review comment on the PR — structured sections, risk callouts, suggested next steps.

**What to say:**
> **This is the moment.** A structured review comment, written by Claude,
> on a real PR. Notice it's not generic — it called out a specific risk,
> flagged a missing test, suggested concrete next steps. And the human
> reviewer still merges — but they start from **this summary** instead of
> a blank diff.

**Transition:** *"Now — that demo was self-contained. What if you've already built useful prompts elsewhere and want to reuse them?"*

---

## Slide 22 — Demo 2 intro: reusing .claude/ subagents  (0:24–0:25)

**On screen:** Heading "what if we could reuse work?" The question of bridging Claude Code subagents in `.claude/` to CI. Answer: "via imports:".

**What to say:**
> **Demo two — a more advanced pattern.** Many of you have already
> invested in Claude Code subagents and skills inside `.claude/` — security
> reviewers, style checkers, triage agents that you use locally in your
> IDE every day. **Question**: can the **same prompt** that helps you
> locally also run **automatically** on every PR in CI? The answer is
> **yes** — and the bridge is **one line of frontmatter**: the `imports:`
> directive. Let me show you how.

**Transition:** *"Here's the bridge, visually."*

---

## Slide 23 — The imports: bridge  (0:25–0:26)

**On screen:** Vertical flow — `.claude/agents/security-reviewer.md` → workflow .md (with imports:) → `gh aw compile` → lock.yml with imported content baked in.

**What to say:**
> Here's how `imports:` works. You have an existing subagent in
> `.claude/agents/security-reviewer.md` — already used by your devs locally
> in Claude Code. You create a **new agentic workflow**, say
> `security-review.md`, that includes one frontmatter line:
> `imports: [.claude/agents/security-reviewer.md]`. When you run
> `gh aw compile`, the imported file's content is **stitched into the
> assembled system prompt**. At runtime, the agent sees that imported
> content as part of its instructions. **One source of truth** — update
> the file once, both your IDE and CI pick it up.

**Transition:** *"Here's what that workflow file actually looks like."*

---

## Slide 24 — The Security Reviewer workflow file  (0:26–0:27)

**On screen:** A full `.md` workflow file with imports: highlighted. About 20 lines. Body says "Apply the security-reviewer rules imported above."

**What to say:**
> The whole workflow file. Notice the **`imports:` line** in the
> frontmatter — that's the bridge. Everything else is standard agentic
> workflow frontmatter. The **body is short** — just two paragraphs —
> because the heavy lifting is in the imported subagent. The workflow
> fires on every PR, applies the imported rules to the diff, posts a
> single comment summarizing findings, and applies labels —
> `security:high` for any red flag, `security:review` for yellow flags.
> Twenty lines, full reuse of existing investment.

**Transition:** *"And here's the payoff that makes this worth talking about."*

### Authoring prompt (if asked "what did you tell Claude to write this?")

> *Paste this into Claude Code in the IDE, in the `gh-aw-demo` repo:*
>
> ```
> We already have a shared skill at .claude/skills/security-review.md that
> defines our security review checklist, severity scale, and per-finding
> output format. Devs use it locally in Claude Code today.
>
> Create a new GitHub Agentic Workflow at
> .github/workflows/pr-security-reviewer.md that REUSES that exact skill
> in CI on every PR — no copy-paste. Trigger on pull_request
> (opened / reopened / synchronize / ready_for_review) plus
> workflow_dispatch with a pr_number input.
>
> Engine: claude. Permissions: contents:read + pull-requests:read only.
>
> Use the imports: frontmatter directive to pull in
> .claude/skills/security-review.md so its content is stitched into the
> agent's system prompt at compile time.
>
> Tools: github MCP allow-list = get_pull_request, get_pull_request_files,
> get_pull_request_diff, list_commits, get_file_contents. Plus bash.
>
> Safe outputs: exactly one add-comment, max: 1.
>
> Body should say: use the imported skill's checklist verbatim, walk the
> diff section-by-section, post one comment starting with "## 🔒 Security
> Review", only flag issues introduced by THIS diff (not pre-existing).
>
> Run gh aw compile and commit both files.
> ```

---

## Slide 25 — Demo 2: the payoff  (0:27–0:28)

**On screen:** Two cards — "In your IDE" (developer uses Claude Code with the subagent) and "In CI on every PR" (workflow imports the same file). Bold line: "Update the prompt once, both surfaces benefit."

**What to say:**
> The payoff. **In your IDE** — a developer asks Claude Code to run the
> security reviewer on a branch. Claude Code loads
> `.claude/agents/security-reviewer.md` automatically. **In CI on every
> PR** — the agentic workflow imports the same file and runs
> automatically. **One prompt, two surfaces.** Update the rules once, both
> the IDE and CI benefit. This is the org-wide payoff: the skills and
> subagents you've built for individual developers become **CI automation
> for the entire team** with one line of frontmatter.

**Transition:** *"So — what's next for us?"*

---

## Slide 26 — Where we go from here  (0:28–0:29)

**On screen:** Two cards. Near-term: hands-on workshop, pilot PR Summarizer, identify candidate .claude/ subagents. Workflows worth exploring: security reviewer, test failure digest, auto-labeler, release notes.

**What to say:**
> Near-term — a **hands-on workshop** where everyone writes their first
> workflow, a **pilot of PR Summarizer** on one team's repo, and
> identifying **two or three `.claude/` subagents** worth bridging to CI.
> On the right, a few patterns worth exploring beyond the demos: a
> security reviewer like we just saw, a daily test-failure digest, a PR
> auto-labeler, a release notes generator. All of these are on the order
> of twenty to forty lines of `.md`.

**Transition:** *"Quick resource pointer."*

---

## Slide 27 — Resources  (0:29–0:30)

**On screen:** Two cards. To read (official repo, our wiki, agentic samples) and To try (clone gh-aw-demo, run gh aw add, open a PR).

**What to say:**
> Quick resource pointer. **To read** — the official `gh-aw` repo on
> GitHub, our internal wiki which now has three pages — a quick start,
> a complete guide, and a case study — and the `agentics` sample
> catalogue for ready-made workflows. **To try after the workshop** —
> clone the `gh-aw-demo` repo, run `gh aw add pr-summarizer` in a
> personal repo, open a PR, watch the magic.

**Transition:** *"Happy to take questions."*

---

## Slide 28 — Questions  (0:30)

**On screen:** "Questions?" Title slide with the demo repo URL and a thank-you.

**What to say:**
> That's the thirty-minute tour. **Questions?**

**Anticipated questions and your answers:**

- **"How much does it cost?"** — Pennies per run. Anthropic API billing rolls
  up to whoever owns the key. GitHub Actions minutes are billed normally.
- **"Can we use Copilot instead of Claude?"** — Yes. Change `engine: claude`
  to `engine: copilot`. Uses an existing Copilot Enterprise entitlement —
  no separate billing.
- **"What if the agent goes rogue?"** — Three layers stop that: read-only
  default token, safe-outputs sandbox, plus a `detection` job that runs a
  second AI pass to detect prompt-injection. The brain has no hands.
- **"Can it modify code?"** — Only via `safe-outputs.create-pull-request`.
  Even then, it opens a PR — a human still merges. There is no "agent
  pushes to main" mode.
- **"Self-hosted runners?"** — Yes, same as any GitHub Action. Set
  `runs-on: self-hosted` in frontmatter.
- **"Is `.claude/` committed in our org?"** — It varies by team. If yes,
  `imports:` works directly. If no, you can either commit it or copy the
  prompts into the workflow body. The pattern still works either way.

---

## Pacing notes

- **Total: 30 minutes for 27 content slides + title.**
- Average ~65 seconds per slide. Some are shorter (screenshots) and some
  longer (mental model, two Claudes, the bridge).
- **Watch the clock at slide 16 (Demo 1 intro).** You should be at the
  19-minute mark there. If you're behind, trim Section 3 (mental model) —
  the "two Claudes" slide can be a 30-second mention rather than 60.
- **Don't skip the "Two Claudes" slide.** Even if compressed, it prevents
  questions later.
- **Pause on slide 21** (Claude's actual comment) — that's the visual
  payoff of Demo 1. Let the audience read.
- **Pause on slide 25** (the payoff) — that's the visual payoff of Demo 2.

---

## What to do if you run short on time

If at slide 22 (Demo 2 intro) you've burned more than 25 minutes:

- **Compress Demo 2** to two slides: the bridge (slide 23) and the
  payoff (slide 25). Skip the workflow-file deep dive (slide 24).
- Move slide 26 ("Where we go") to your follow-up email instead.
- Land at Q&A by minute 29.

If you have **extra time** at the end:

- Briefly demo opening the actual `gh-aw-demo` repo in a browser tab.
- Show the team wiki page if it's already published.
- Take more questions.

---

# Appendix — Authoring Prompts for All Workflows in the Repo

> The repo ships with **5 agentic workflows**. The presentation only walks
> through PR Summarizer (Demo 1) and PR Security Reviewer (Demo 2), but the
> other 3 are committed so audience members can browse them after the talk.
> If anyone asks *"how would I create one of those?"*, paste the matching
> prompt below into Claude Code in the IDE.

---

## A1 — PR Reviewer (`.github/workflows/pr-reviewer.md`)

**Purpose:** finds real defects in the diff (not a summary). Pairs with the
PR Autofixer below to form the 3-agent Demo 1 story
(*summarize → review → optionally autofix*).

**Authoring prompt:**

```
Create a new GitHub Agentic Workflow at .github/workflows/pr-reviewer.md
for the gh-aw-demo FastAPI repo. It is a SIBLING to pr-summarizer.md —
summarizer describes the change, reviewer finds defects in it.

Trigger on pull_request (opened / reopened / synchronize / ready_for_review)
plus workflow_dispatch with pr_number input.

Engine: claude. Permissions: contents:read + pull-requests:read only.
Tools: github MCP allow-list = get_pull_request, get_pull_request_files,
get_pull_request_diff, list_commits, get_file_contents. Plus bash.

Safe outputs: exactly one add-comment, max: 1.

Body should instruct Claude to post one comment starting with "## 🤖 PR
Review" containing a bulleted list of findings. Each finding uses this
exact shape:

  - 🔴/🟡/🟢 **<title>** — `<file>:<line>`
    <problem in one sentence>
    <fix in one sentence>

Severity rules: 🔴 = breaks tests / breaks API / data loss / security hole;
🟡 = likely bug, missing validation, swallowed exception; 🟢 = style nits.

Specifically look for: new endpoints in app/main.py without tests,
Pydantic model/usage mismatches, NoteStore invariant breaks, missing
input validation, leftover print/broad except. End the comment with
either "✅ Ready to merge after addressing 🔴/🟡 items." or
"⚠️ Blocking issues — please fix 🔴 items before merge."

Cap at ~500 words. Run gh aw compile and commit both files.
```

---

## A2 — PR Autofixer (`.github/workflows/pr-autofixer.md`)

**Purpose:** human applies the `ai-fix` label after reading the reviewer's
comment → autofixer reads the comment, applies fixes, pushes a commit.
This is the **hands** that the reviewer (brain) cannot have.

**Authoring prompt:**

```
Create a new GitHub Agentic Workflow at .github/workflows/pr-autofixer.md
for the gh-aw-demo repo. It is the "hands" companion to pr-reviewer.md.

Trigger ONLY on pull_request: [labeled], and guard with
`if: github.event.label.name == 'ai-fix'` so other label adds don't burn
a Claude run.

Engine: claude. Permissions: contents:write + pull-requests:write (it
needs to push commits and comment).

Tools: github MCP allow-list = get_pull_request, get_pull_request_files,
get_pull_request_diff, get_pull_request_comments, list_commits,
get_file_contents. Plus bash.

Safe outputs: push-to-pull-request-branch max: 1, and add-comment max: 1.

Body should instruct Claude to:
  1. Fetch the PR diff AND existing PR comments.
  2. Find the most recent comment starting with "## 🤖 PR Review".
  3. Apply fixes ONLY for 🔴 and 🟡 findings — ignore 🟢 nits.
  4. Keep changes minimal (touch only the called-out lines, no
     reformatting, no renames, no requirements.txt edits, no CI edits).
  5. If a fix would change a public endpoint shape in app/main.py,
     SKIP it and list it under Skipped — humans decide API changes.
  6. Push one commit (or grouped commits) via the safe-output.
  7. Post one summary comment starting with "## 🤖 Autofix Applied"
     with sections: Fixed / Skipped / Verify.
  8. If no PR Review comment exists, post "## 🤖 Autofix Skipped" and
     push nothing.

Stop after one push — no self-triggering loops.

Run gh aw compile and commit both files.
```

---

## A3 — TFS Ticket Researcher (`.github/workflows/tfs-ticket-researcher.md`)

**Purpose:** the third demo. Take a TFS work item ID via
`workflow_dispatch`, fetch the ticket from on-prem TFS, map it to this
repo, and open a GitHub issue with a structured research doc. Does NOT
implement the change.

**Authoring prompt:**

```
Create a new GitHub Agentic Workflow at
.github/workflows/tfs-ticket-researcher.md for the gh-aw-demo repo.

It is triggered manually via workflow_dispatch with one required string
input: ticket_id (e.g. 2913577).

Engine: claude. Permissions: contents:read + issues:write.

Env vars (set at workflow level):
  TFS_BASE_URL: https://tfs.realpage.com/tfs/Realpage
  TFS_PAT:      ${{ secrets.TFS_PAT }}    # already added to repo secrets

Tools: bash allow-list curl:* and jq:*. Plus github MCP for
get_file_contents and list_pull_requests.

Safe outputs: create-issue max: 1.

Body should instruct Claude to:
  1. Call TFS REST API:
       curl -s -u ":$TFS_PAT" \
         "$TFS_BASE_URL/_apis/wit/workitems/${TICKET_ID}?api-version=7.0&\$expand=all"
     then jq the response to extract title, state, type, description,
     repro steps, acceptance criteria. Never log $TFS_PAT.
  2. Read up to ~6 relevant files in this repo (app/main.py,
     app/models.py, app/store.py, tests/test_notes.py) to understand
     what code would change.
  3. Open ONE GitHub issue via create-issue with:
       Title: "[Research] TFS <id> — <ticket title>"
       Body: sections — Source ticket / What the ticket asks for /
             Acceptance criteria / Proposed change in this repo (files to
             touch + suggested endpoint shape) / Risks & open questions /
             Test plan / Out of scope.
  4. Never push code, never open a PR. Strip HTML tags from TFS
     description before quoting. Cap issue body at ~600 words.

If curl returns 401 or 404, still open the issue but with a clear
"failed to fetch ticket" note instead of inventing content.

Run gh aw compile and commit both files.
```

---

## A4 — The shared skill (`.claude/skills/security-review.md`)

**Purpose:** the imported content that pr-security-reviewer.md uses.
Lives outside `.github/workflows/` because it is also usable directly by
devs inside Claude Code in the IDE.

**Authoring prompt:**

```
Create a reusable skill at .claude/skills/security-review.md for the
gh-aw-demo repo. It will be imported by an agentic workflow AND used
directly in Claude Code by developers, so it must be self-contained.

Frontmatter: name + description only (it's a skill, not a workflow).

Body: a security review checklist tailored to Python / FastAPI services.
Define:
  - The exact per-finding output format:
      - 🔴/🟡/🟢 **<title>** — `<file>:<line>`
        <risk in one sentence>
        <fix in one sentence>
  - A severity scale (🔴 high / 🟡 medium / 🟢 low) with concrete
    examples for each level.
  - Six checklist sections to walk: Input handling, Authn/authz, Data
    exposure, Dependencies & supply chain, Secrets & config, CI /
    workflow changes.
  - A required one-line verdict at the end:
    "✅ No security concerns found." or "⚠️ <N> findings — see above."

Also update .gitignore so .claude/* is ignored but .claude/skills/ is
explicitly allowed (so the skill IS committed but local agent state is
not).
```

---

## Tips when you give these prompts to Claude Code yourself

- Always tell Claude Code which **engine** to use (`claude`) and which
  **safe-outputs** are allowed. That removes ambiguity in the generated
  frontmatter.
- Always end with *"run gh aw compile and commit both files"* — otherwise
  Claude often produces only the `.md` and you forget the lock file.
- For workflows that need a secret (like `TFS_PAT`), name the secret
  explicitly in the prompt. Claude won't guess it correctly.
- If the generated workflow looks too long, ask Claude to *"tighten the
  body — under 80 lines, no preamble"*. Shorter prompts → cheaper, faster
  runs.
