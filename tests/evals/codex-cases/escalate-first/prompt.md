---
name: escalate-first
description: Codex only — when told directly to prepare (D-65), run warmup outside the sandbox (with escalation) from the start. No wasted run inside the sandbox
tags: [codex, permission]
max_turns: 25
timeout_seconds: 300
env:
  EVAL_PREVUE_SCENARIO: unready
---

Screen.kt(app/src/main/kotlin/Screen.kt) 프리뷰를 보려는데 빌드 설정부터 읽어 와야 한대. 준비해 줘.
