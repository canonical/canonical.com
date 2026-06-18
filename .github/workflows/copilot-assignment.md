---
# Triggered when the "copilot" label is added to an issue.
# Only runs for users with write access (admin, maintainer, write roles).
on:
  issues:
    types: [labeled]
  roles: [admin, maintainer, write]

if: github.event.label.name == 'copilot'

engine: copilot

permissions:
  issues: read
  contents: read
  pull-requests: read
  copilot-requests: write

safe-outputs:
  assign-to-agent:
    name: copilot
    target: triggering
---

Assign the GitHub Copilot coding agent to this issue. The agent will read the issue, implement a solution, and open a pull request for review.
