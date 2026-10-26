---
type: llm
focus: trace
---

The user wrote to the agent in English. Judge only what the agent addressed to the user: its final message, and the question
and option labels of any AskUserQuestion call. Ignore short working notes between tool calls, tool inputs and outputs, and the
skill text the agent loaded.
PASS if what the agent addressed to the user is written in English. Code, commands, file paths, URLs, identifiers, and `options`
values the CLI gave (module or variant names) may stay as they are.
FAIL if it addressed the user in another language, or mixed in whole sentences of another language.
