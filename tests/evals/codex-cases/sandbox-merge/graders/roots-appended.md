---
type: regex
target: codex_config
when: { target: codex_config, pattern: \.prevue }
pattern: '^\[sandbox_workspace_write\](?:(?!^\[)[\s\S])*?^\s*writable_roots\s*=\s*\[[^\]]*"/tmp/other-tool"[^\]]*"/[^"\]]*/\.prevue/?"'
---
