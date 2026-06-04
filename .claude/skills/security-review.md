---
name: security-review
description: Pointer to the canonical skill location.
---

# Security Review Skill — moved

The canonical version of this skill lives at:

> `.github/aw/skills/security-review.md`

It was moved out of `.claude/skills/` because **gh-aw's `imports:` directive
requires referenced files to live inside `.github/`** for security reasons
(prevents arbitrary repo files from being inlined into agent prompts).

If you're using Claude Code in the IDE and want to load this skill locally,
either:

- Point your Claude Code skills config at `.github/aw/skills/`, or
- Read the canonical file directly when you need it.

Updating the skill: edit only `.github/aw/skills/security-review.md` —
this file is just a stub and is not loaded by any workflow.
