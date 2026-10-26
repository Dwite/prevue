---
name: entry-trigger
description: ① a mockup or viewing request invokes the entry skill (prevue). Hands over the viewer address as a link
tags: [nfr15, trigger]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: ready
---

app/src/main/kotlin/Screen.kt 의 Greeting 화면이 지금 어떻게 보이는지 띄워 줘.
