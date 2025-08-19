## Action Plan

### P0 (Today)
1. Install app deps so typecheck passes
   - Owner: FE
   - Command: `pnpm -C /Users/gregpaulsen/Desktop/PaulyOps_Main/app install`
2. Provide DB URL and run migrations
   - Owner: BE
   - Steps:
     - Copy `.env.local.example` → `.env.local` and set `DATABASE_URL`
     - `pnpm -C /Users/gregpaulsen/Desktop/PaulyOps_Main/app db:gen`
     - `pnpm -C /Users/gregpaulsen/Desktop/PaulyOps_Main/app db:migrate`
3. Verify dev server boots and page loads
   - Owner: FE
   - `pnpm -C /Users/gregpaulsen/Desktop/PaulyOps_Main/app dev`

### P1 (This week)
1. Add Biome lint to `app/`
   - Owner: FE
   - Use root Biome or add per-app config; wire `pnpm -C app lint` to Biome.
2. Harden Supabase MCP
   - Owner: BE
   - Replace `exec_sql` with migrations or PostgREST limited endpoints. Add dry-run flag.
3. Add basic AuthGuard and `/api/auth/session` smoke test page.
   - Owner: FE

### P2 (Later)
1. Add RLS notes and policies for `projects` and future tables.
2. Add indexes on `org_id`, `created_at`.
3. Add GH Actions: Node 20, pnpm i, typecheck, build.


