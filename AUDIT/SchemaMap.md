## Tables

### projects
- id: uuid, primary key, defaultRandom()
- orgId: uuid, not null
- name: text, not null
- createdAt: timestamp, default now

Notes:
- Multi-tenant: `orgId` present (good). Add RLS in Supabase to enforce `org_id = auth.uid()'s org` as appropriate.
- Indexes suggested: `(org_id)`, `(created_at)`.
- FK suggested: `org_id` → `orgs.id` (when orgs table exists).


