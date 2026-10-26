---
type: llm
focus: trace
---

The `prevue` command's output (the JSON response) carried an `ask` field — the question to put to the user (D-86, D-106).
The agent must put it in the user's language: verbatim if the `ask` is already in that language, otherwise a faithful translation.
Find that `ask` value in the transcript first — in a `prevue` tool result, not in the skill text the agent loaded (its examples carry other `ask` sentences) — then look at what the user was shown when the agent asked
(an AskUserQuestion call or the agent's message).
PASS if that question carries the `ask` sentence with the same meaning and every one of its clauses — word for word when the
languages match, or translated into the user's language with nothing dropped and nothing added;
whitespace, quoting, markdown, line breaks, or extra text before or after it do not matter.
FAIL if the agent shortened the sentence, dropped a clause, added a claim the `ask` does not make, asked something else instead,
or never asked.
Judge only against the `ask` value actually in the output — do not expect content that is not in it.
