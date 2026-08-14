---
description: Assigns the GitHub Copilot coding agent to issues labelled "copilot"
emoji: 🤖
on:
  issues:
    types: [labeled]
  roles: [admin, maintainer, write]

if: github.event.label.name == 'copilot'

permissions:
  issues: read
  contents: read
  pull-requests: read
  copilot-requests: write

tools:
  github:
    mode: gh-proxy
    toolsets: [default]
  cli-proxy: true

safe-outputs:
  assign-to-agent:
    name: copilot
    target: triggering
---

Assign the GitHub Copilot coding agent to this issue. The agent will read the issue, implement a solution, and open a pull request for review.
