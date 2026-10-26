---
type: llm
focus: trace
---

The tool reported that both the components (a one-time download) and the project's build settings are missing.
PASS if, before any `prevue setup` or `prevue warmup` command was run, the agent put one approval question to the user that
covers both preparations together (downloading components and reading the build settings), then stopped and waited.
Restating that same question in a closing message at the end of the turn is still one question.
Running no setup/warmup at all after asking also PASSES.
FAIL if it ran `prevue setup` or `prevue warmup` before asking, asked two separate questions that each need their own answer
(one per preparation), or never asked.
