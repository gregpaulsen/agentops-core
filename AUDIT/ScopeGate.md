## Scope Gate

### Core Platform (must-haves now)
- Multi-tenant model + RLS: PARTIAL (orgId present on `projects`, RLS pending)
- Auth (Google) + session: SCAFFOLDED (needs creds + test)
- tRPC contracts: `projects` present; `reports`/`uploads` can be stubbed via MCP Supabase
- MCP → dev accelerators only: OK

Decision: Trim scope until Core all green. Ship Core first, then add-on agents.

### Add-on Agents
- Inbox Cleaner, NDVI, etc.: LATER

### Dev-only Tools
- Figma/Google/Rive MCP: keep dev-only, not prod

### 2-sprint Plan
- Sprint 1: P0/P1 from ActionPlan, add RLS and indexes, add `reports` table/router
- Sprint 2: Basic UI for projects/reports CRUD, token sync from Figma MCP


