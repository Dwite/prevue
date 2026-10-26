---
name: landing-through-warmup
description: a request that approved preparing the preview finishes from the landing page to the preview with next's warmup --show, and runs no duplicate start
tags: [nfr15, preparation]
plugins: ["../.."]
max_turns: 25
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, AskUserQuestion, TodoWrite]
env:
  EVAL_PREVUE_SCENARIO: unready
---

app/src/main/kotlin/Screen.kt 프리뷰를 띄워 줘. 필요한 빌드 설정 읽기도 승인하니 준비부터 화면을 띄우는 것까지 진행해 줘.
