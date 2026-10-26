---
name: selection-empty
description: ⑤ "this" reads selection first, and if it's empty, asks the person to point instead of guessing an edit
tags: [nfr15, pointing]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: selection-empty
---

app/src/main/kotlin/Screen.kt 프리뷰를 보고 있는데, 이거 여백 좀 줄여 줘.
