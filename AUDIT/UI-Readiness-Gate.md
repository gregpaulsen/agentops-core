## UI Readiness Gate

### Green
- App scaffold present (Next 14 App Router, Tailwind, tRPC, Drizzle, NextAuth).
- MCP servers scaffolded; paths aligned for scaffolding outputs.

### Blockers
- Typecheck failing due to missing installed deps in `app/`. Fix: `pnpm -C app install`.
- Database URL not set; migrations blocked. Fix: set `DATABASE_URL` in `app/.env.local` and `pnpm -C app db:migrate`.
- Auth not verified end-to-end. Fix: set Google creds and smoke test `/api/auth/session`.

### Verdict
Not ready until P0 blockers are cleared.


