---
name: first-install
description: first time on this machine — ask about downloading components and reading build settings once, as one ask question, and run no setup · warmup before asking (D-86)
tags: [nfr15, approval]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: first-install
---

app/src/main/kotlin/Screen.kt 프리뷰 띄워 줘.
