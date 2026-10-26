---
name: help-picks-command
description: ⑥ picks a command the skill doesn't mention from the help alone — redrawing one card is prevue card <index> --force
tags: [d55, help]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: ready
---

app/src/main/kotlin/Screen.kt 보드가 떠 있어. 3번 카드만 강제로 다시 그려 줘.
