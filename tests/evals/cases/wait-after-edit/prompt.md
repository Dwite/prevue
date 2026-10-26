---
name: wait-after-edit
description: ④ after editing code, get that save's image with prevue wait (not calling show again · not sleep)
tags: [nfr15, loop]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: ready
---

app/src/main/kotlin/Screen.kt 의 Greeting 바깥 패딩을 16dp 에서 8dp 로 줄이고, 바뀐 화면을 프리뷰로 확인해 줘.
