## Render.com Checklist

### Build
```
pnpm install --frozen-lockfile
pnpm --dir /Users/gregpaulsen/Desktop/PaulyOps_Main/app db:gen
pnpm --dir /Users/gregpaulsen/Desktop/PaulyOps_Main/app db:migrate
pnpm --dir /Users/gregpaulsen/Desktop/PaulyOps_Main/app build
```

### Start
```
pnpm --dir /Users/gregpaulsen/Desktop/PaulyOps_Main/app start
```

### Env Vars
- DATABASE_URL
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- NEXTAUTH_URL
- YOUTUBE_API_KEY (optional)

### Health Checks
- `/` should return 200
- `/api/trpc` should not 404

### Optional render.yaml (pseudo)
```
services:
  - type: web
    name: paulyops-app
    env: node
    plan: starter
    buildCommand: |
      pnpm install --frozen-lockfile
      pnpm -C app db:gen && pnpm -C app db:migrate
      pnpm -C app build
    startCommand: pnpm -C app start
    envVars:
      - key: DATABASE_URL
      - key: GOOGLE_CLIENT_ID
      - key: GOOGLE_CLIENT_SECRET
      - key: NEXTAUTH_URL
      - key: YOUTUBE_API_KEY
```


