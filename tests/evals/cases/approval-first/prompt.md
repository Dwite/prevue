---
name: approval-first
description: ③ when show exits 3, ask with the response's ask sentence before running Gradle (warmup) — no internal skill (D-86)
tags: [nfr15, approval]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: unready
---

app/src/main/kotlin/Screen.kt 프리뷰 띄워 줘.
