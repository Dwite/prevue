---
name: choose-app
description: two apps to borrow resources from — ask choosing the app and approving the build-settings read as one ask question, showing the candidates (options) as choices. No warmup before the answer (D-86)
tags: [nfr15, approval]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: choose-app
---

app/src/main/kotlin/Screen.kt 프리뷰 띄워 줘.
