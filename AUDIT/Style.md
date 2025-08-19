## Static & Style Findings

### TypeScript
- `pnpm -C app exec tsc --noEmit` reports missing module type declarations for:
  - @trpc/*, @tanstack/react-query, next-auth, @auth/drizzle, framer-motion, @rive-app/react-canvas, axios, postgres
- Fix: `pnpm -C app install` to ensure dependencies are present (they are in package.json) and re-run tsc.

### Linting
- Monorepo root uses Biome. `app/` has no lint script wired to Biome.
- Quick PR plan:
  - Add script in `app/package.json`: `"lint": "biome check ."`
  - Or add `.biome.json` in `app/` to customize rules.


