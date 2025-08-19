## tRPC Routers

### projectRouter
- list
  - input: none
  - output: `projects[]`
  - cache: suggest `staleTime: 5_000`
- create
  - input: `{ orgId: string, name: string }`
  - output: inserted row(s)
  - errors: DB insert failures

### resourcesRouter
- youtubeGuides
  - input: `{ q: string(min 2) }`
  - output: `{ id, title, channel }[]`
  - cache: external API; suggest `staleTime: 60_000`

### appRouter
Combines: `project` (+ add `resources` when wired in `app/src/server/routers/index.ts`).


