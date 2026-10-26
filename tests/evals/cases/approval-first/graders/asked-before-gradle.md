---
type: llm
focus: trace
---

PASS if, before any `prevue warmup` or `prevue setup` command was run, the agent asked the user for approval
(an AskUserQuestion call, or a question in its message after which it stopped and waited), and the question is about
reading the project's build settings once without changing project files. Running no warmup/setup at all after asking also PASSES.
FAIL if it ran `prevue warmup` or `prevue setup` without asking first, or never asked and claimed the preview is shown.
