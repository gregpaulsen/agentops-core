| NAME | Scope | Required | Example | Notes |
|---|---|---|---|---|
| DATABASE_URL | app | yes | postgres://USER:PASSWORD@HOST:PORT/DB | Drizzle/PG client connection |
| GOOGLE_CLIENT_ID | app | yes | your_client_id.apps.googleusercontent.com | NextAuth Google provider |
| GOOGLE_CLIENT_SECRET | app | yes | your_client_secret | NextAuth Google provider |
| NEXTAUTH_URL | app | yes | http://localhost:3000 | Used by NextAuth callbacks |
| YOUTUBE_API_KEY | app | no | AIza... | For `searchGuides` util |
| SUPABASE_URL | mcp-supabase | yes | https://YOUR_PROJECT.supabase.co | Supabase client base URL |
| SUPABASE_SERVICE_ROLE | mcp-supabase | yes | service_role_key | Only for server-side MCP ops |
| SCHEMA_OUT_DIR | mcp-supabase | no | ../app/src/server/db/schema | Output path for schema files |
| MIGRATIONS_OUT_DIR | mcp-supabase | no | ../app/drizzle | Drizzle migrations dir |
| FIGMA_PERSONAL_TOKEN | mcp-figma | yes | figd_... | Figma API token |
| FIGMA_FILE_KEY | mcp-figma | yes | abcDEF123 | Target Figma file key |
| TAILWIND_CONFIG_PATH | mcp-figma | no | ../app/tailwind.config.ts | Tailwind config path to patch |
| COMPONENTS_OUT_DIR | mcp-figma | no | ../app/src/components | Where to write generated components |
| RIVE_ASSETS_DIR | mcp-rive | no | ../app/public/rive | Directory for `.riv` files |
| GOOGLE_REDIRECT_URI | mcp-google | yes | http://127.0.0.1:8787/callback | OAuth redirect URI |
| GOOGLE_SCOPES | mcp-google | no | space-separated scopes | OAuth consent scopes |


