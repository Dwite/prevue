---
name: unbaked-start
description: Codex only — the first start after an upgrade calls Gradle to bake and needs escalation (startNeedsEscalation). Run it outside the sandbox from the start as the response says, and hand over the viewer address
tags: [codex, permission]
max_turns: 25
timeout_seconds: 300
env:
  EVAL_PREVUE_SCENARIO: unbaked
---

app/src/main/kotlin/Screen.kt 프리뷰 띄워 줘.
