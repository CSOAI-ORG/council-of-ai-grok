# npm README fix (csoai-gspc-mcp 0.1.1)

Replace the stale “not yet published to npm (checked 2026-08-27)” block with:

```sh
npx -y csoai-gspc-mcp
```

Claude: `claude mcp add gspc -- npx -y csoai-gspc-mcp`  
Cursor: `"command": "npx", "args": ["-y", "csoai-gspc-mcp"]`  
Grok: `[mcp_servers.gspc-npm] command = "npx"` / `args = ["-y", "csoai-gspc-mcp"]`

PR: https://github.com/CSOAI-ORG/councilof-ai/pull/883  
After merge: `cd mcp/gspc-server && npm publish --access public` (version already 0.1.1 in the PR).
