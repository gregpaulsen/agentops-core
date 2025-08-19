## MCP Tool Contracts

### google-oauth
- get_google_tokens(scopes?: string) → tokens JSON

### supabase
- db_create_table(sql: string)
- db_generate_drizzle_schema(tableName: string, columns: { name: string, type: string, optional?: boolean }[])
- db_crud_scaffold(tableName: string, routerOutDir: string)

### figma
- figma_pull_tokens() → append note to Tailwind config (placeholder)
- figma_component_to_react(name: string) → writes component file

### rive
- rive_list() → list .riv files
- rive_download(name: string, url: string) → saves placeholder .riv file

## Risks & Hardening
- Supabase raw `exec_sql` RPC is risky. Prefer migrations or whitelisted SQL operations. Add dry-run and confirmation gates.
- Figma Tailwind patch should be explicit and idempotent.


