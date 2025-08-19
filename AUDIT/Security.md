## Security & Compliance Pre-flight

- Secrets in env files only; no hard-coded secrets found.
- RLS: add Supabase RLS policies for multi-tenant data (`projects`).
- Roles/Permissions: add org-based checks in routers where appropriate.
- Logging: centralize error logging; redact PII.
- Audit trail: recommend `events` table for important mutations.
- Key rotation: schedule rotation for OAuth and DB credentials.


