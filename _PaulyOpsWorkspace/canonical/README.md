# PaulyOps - Enterprise Operations Platform

A multi-tenant, white-label operations platform with intelligent document processing, agent automation, and analytics.

## 🏗 Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Next.js API routes with Prisma ORM
- **Database**: PostgreSQL (Neon)
- **Authentication**: NextAuth.js with Google OAuth
- **Payments**: Stripe with subscription management
- **Agents**: Modular, sandboxed agent framework
- **Desktop**: Electron-based installer with Dropzone integration

## 📁 Project Structure

```
PaulyOps/
├── apps/
│   ├── ui/                    # Next.js 14 application
│   └── dropzone-watcher/      # Desktop file monitoring service
├── agents/
│   ├── inbox-cleaner/         # Email processing agent
│   ├── ndvi-processor/        # Agricultural data processing
│   └── vendor-router/         # Vendor document routing
├── packages/
│   ├── shared/                # Shared utilities and types
│   └── security/              # RBAC, sandboxing, audit logging
├── installer/
│   └── electron/              # Cross-platform installer
├── configs/
│   └── routing/               # Dropzone routing rules
└── docs/                      # Documentation
```

## 🚀 Quick Start

### Development

```bash
cd apps/ui
npm install
npm run dev
```

### Desktop Installation

1. Download the installer for your platform
2. Run the installer
3. PaulyOps will be created on your Desktop
4. Dropzone will be set up for file processing

## 🔧 Configuration

- Environment variables: See `.env.example`
- Routing rules: `configs/routing/rules.yaml`
- Agent permissions: `packages/security/rbac.ts`

## 📊 Features

- **Multi-tenant**: Support for multiple organizations
- **White-label**: Brand-agnostic design
- **Agent Framework**: Pluggable, secure automation
- **Dropzone**: Intelligent file routing and processing
- **Analytics**: Usage tracking and insights
- **SOC 2 Ready**: Security and compliance features

## 🛡 Security

- RBAC enforcement on all operations
- Agent sandboxing and permission controls
- Audit logging for compliance
- SOC 2 alignment features

## 📈 Roadmap

- Sprint 1 ✅: Auth, Stripe, Prisma, Gmail digest, RBAC
- Sprint 2 🚧: Production deployment, onboarding, trials, support, analytics
- Future: Advanced agents, integrations, enterprise features
