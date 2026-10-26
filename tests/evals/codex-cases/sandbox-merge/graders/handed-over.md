---
type: regex
target: last_message
unless: { target: codex_config, pattern: \.prevue }
pattern: 'network_access\s*=\s*true[\s\S]*\.prevue|\.prevue[\s\S]*network_access\s*=\s*true'
---
