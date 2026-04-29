---
description: Run the health-checker subagent over the wiki.
---

Read CLAUDE.md.

Delegate to the `health-checker` subagent.

Health check the wiki:
- missing linked pages
- orphan pages
- contradictions (tag P0/P1/P2)
- stale API claims (older than 90 days)
- concepts missing their own page
- outputs that should be promoted to wiki

Use Context7 only for API-sensitive claims.

Update `wiki/health.md`.
Append to `wiki/log.md`.
Suggest 3 new articles.
