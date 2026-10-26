---
name: sandbox-merge
description: Codex only — the user consented up front to adding sandbox settings. Keep the settings already touched (other keys · comments · other paths in the same table), merge only network_access and ~/.prevue, tell them to restart and stop
tags: [codex, sandbox]
max_turns: 25
timeout_seconds: 300
env:
  EVAL_PREVUE_SCENARIO: sandbox-merge
---

app/src/main/kotlin/Screen.kt 프리뷰 띄워 줘. Codex 샌드박스 설정이 필요하면 내가 동의하니까 다시 묻지 말고 바로 넣어 줘.
