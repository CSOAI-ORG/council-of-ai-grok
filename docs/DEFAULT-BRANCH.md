# Default branch — flip `main` → `master`

`ALIGNMENT.md` in `CSOAI-ORG/councilof-ai` already records the split:

| Branch | Role |
|---|---|
| `master` | Production. Vite SPA. Live site. ALIGNMENT.md, MCP, OS. |
| `main` | GitHub default. Diverged experiment. Agents land here by mistake. |

Grok Build, Claude Code, Cursor, and `git clone` without `-b` all follow the **GitHub default branch**. Until it is `master`, every new agent session starts on the wrong lane.

## Do this in GitHub UI (owner)

1. Open https://github.com/CSOAI-ORG/councilof-ai/settings
2. Branches → Default branch → switch to `master`
3. Confirm

## Do this with gh (owner token)

```bash
gh repo edit CSOAI-ORG/councilof-ai --default-branch master
```

REST:

```bash
gh api -X PATCH repos/CSOAI-ORG/councilof-ai -f default_branch=master
```

## After the flip

```bash
git clone https://github.com/CSOAI-ORG/councilof-ai.git
cd councilof-ai
git branch --show-current   # expect master
```

Update clone instructions in README, `llms-install.md`, Smithery listings, and any agent card that still says `main`.

## What this session could not do

The connected GitHub token can read the account (`CSOAI-ORG`) but cannot create repos, branches, or files (403). Flip the default branch from Nick's own logged-in session.

## Optional: archive noise

Hundreds of utility MCP repos dilute the measurement story. After the branch flip, mark non-Layer-0 utility MCPs as archived or move them under a `legacy-mcp` topic so `/council` and `councilof-ai` stay the front door.
