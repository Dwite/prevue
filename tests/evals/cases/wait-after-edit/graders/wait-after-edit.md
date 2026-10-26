---
type: tool_order
before: { tool: Edit }
after: { tool: Bash, input_match: '(prevue|\$\{?\w+\}?)\s+wait\b' }
---
