# PaulyOps App

Blazingly fast operations platform with AI-powered automation.

## Features

- **Next.js 14** with App Router
- **TypeScript** for type safety
- **tRPC** for type-safe APIs
- **TanStack React Query** for data fetching
- **Drizzle ORM** with PostgreSQL
- **Framer Motion** & **GSAP** for animations
- **Rive** for interactive animations
- **Tailwind CSS** for styling
- **shadcn/ui** components

## Getting Started

1. Install dependencies:
   ```bash
   pnpm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your values
   ```

3. Set up the database:
   ```bash
   pnpm db:generate
   pnpm db:migrate
   ```

4. Start the development server:
   ```bash
   pnpm dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── api/            # API routes
│   ├── globals.css     # Global styles
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── providers.tsx   # React providers
├── components/         # React components
├── lib/               # Utilities and configurations
└── server/            # Server-side code
    ├── db/            # Database configuration
    ├── routers/       # tRPC routers
    ├── trpc.ts        # tRPC configuration
    └── youtube.ts     # YouTube API integration
```

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run linter
- `pnpm db:generate` - Generate database migrations
- `pnpm db:migrate` - Run database migrations

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Database**: PostgreSQL with Drizzle ORM
- **Authentication**: NextAuth.js
- **API**: tRPC
- **State Management**: TanStack React Query
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion, GSAP, Rive
- **External APIs**: YouTube Data API

## MCP Integration

This app is designed to work with MCP (Model Context Protocol) servers for development:

- **Google OAuth MCP**: Get OAuth tokens for development
- **Supabase MCP**: Database operations and schema generation
- **Figma MCP**: Design token and component generation
- **Rive MCP**: Animation asset management

## Deployment

The app is configured for deployment on Render.com with:

- **Build Command**: `pnpm install && pnpm db:generate && pnpm db:migrate && pnpm build`
- **Start Command**: `pnpm start`
- **Environment**: Node.js 20
