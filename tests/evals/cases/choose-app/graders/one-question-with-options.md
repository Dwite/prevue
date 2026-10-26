---
type: llm
focus: trace
---

The tool reported that the screen can be drawn with either of two apps' resources (`:app`, `:wear` in `options`) and that the
build settings must be read once.
PASS if, before any `prevue warmup` command was run, the agent put one question to the user that lets them pick `:app` or `:wear`
(both shown as choices) and says the build settings will be read — then stopped and waited. A stop/cancel choice is fine.
Restating that same question in a closing message at the end of the turn (for example "please answer the question above") is
still one question, not two.
FAIL if it ran `prevue warmup` before the user answered, picked an app itself, asked the app choice and the approval as two
separate questions that each need their own answer, or did not show both candidates.
