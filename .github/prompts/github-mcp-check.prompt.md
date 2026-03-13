---
name: github-mcp-check
description: "Verify GitHub MCP is connected by listing repositories visible to the authenticated user."
agent: agent
---

Goal:
- Confirm the GitHub MCP server is connected and authorized.

Steps:
1. Call GitHub MCP tools to retrieve the current authenticated user.
2. List repositories visible to that user.
3. Include repository name, visibility, and URL in the output.
4. Highlight whether se333-demo is present.

Output format:
- Authenticated user: <login>
- Repository count: <n>
- Repositories:
  - <owner>/<name> | <visibility> | <url>
- se333-demo present: <yes/no>
