# Context7 Setup Notes

Context7 supplies current external API documentation through MCP. It does not replace the wiki.

## Claude Code

```powershell
npx ctx7 setup --claude
```

Or manually:

```powershell
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```

Verify inside Claude Code:

```text
/mcp
```

## Codex

### No-admin setup, preferred on Windows

If Node.js / `npx` is not installed, use Codex's streamable HTTP MCP support. This does not require admin rights, Node, npm, or npx.

```powershell
codex mcp add context7 --url https://mcp.context7.com/mcp
codex mcp login context7
codex mcp list
```

Expected result:

```text
Name      Url                           Status   Auth
context7  https://mcp.context7.com/mcp  enabled  OAuth
```

This writes the user-level config:

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
```

Verified on Windows without admin permissions: 2026-04-30.

### Local stdio setup with npx

If Node.js / `npx` is already available, add this to `C:\Users\<you>\.codex\config.toml`:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

If Windows cannot find npx, use the full path:

```toml
[mcp_servers.context7]
command = "C:\\Program Files\\nodejs\\npx.cmd"
args = ["-y", "@upstash/context7-mcp"]
```

## Library ID resolution

Context7 uses identifiers like `/upstash/context7` or `/vercel/next.js`.

Workflow:
1. Call `resolve-library-id` with the library name.
2. Cache the returned ID in `wiki/local_ai_workflow/context7_usage.md` under the table.
3. Use the cached ID for future calls.

## Caching strategy

After Context7 returns a useful answer:

1. Copy the relevant excerpt into `wiki/local_ai_workflow/<library>_notes.md`.
2. Record the date and library version.
3. Future reads check the wiki page first.
4. Refresh from Context7 only if the entry is older than 90 days or the user reports a version bump.

## Fallback strategy

- If Context7 is unavailable: fall back to web search of the library's official documentation URL.
- If both are unavailable: state the uncertainty and proceed with the most recent wiki entry, marked as potentially stale.

## Usage rule

Context7 is for current external API documentation only.
The wiki is for project memory.
The list of allowed Context7 libraries lives in `wiki/local_ai_workflow/context7_usage.md`. Update there.
