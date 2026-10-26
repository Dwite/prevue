---
name: approval-first-en
description: approval-first with an English prompt — the CLI's ask is Korean, so the agent puts it in English with every clause and nothing added, before any Gradle (D-86, D-106)
tags: [nfr15, approval]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: unready
---

Show me the preview for app/src/main/kotlin/Screen.kt.
