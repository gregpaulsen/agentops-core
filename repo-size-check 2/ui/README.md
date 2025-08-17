# PaulyOps UI

A tenant-aware, white-label Next.js 14 UI for the PaulyOps multi-tenant platform.

## Features

- **Multi-tenant Support**: Dynamic theming and feature flags based on tenant
- **Real-time Updates**: WebSocket integration for live dashboard updates
- **Managed Services**: Toggleable service management with plan-based restrictions
- **File Management**: Upload, download, and manage files
- **Backup Operations**: Create and restore backups
- **Activity Monitoring**: Real-time operation tracking
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: TanStack Query
- **Charts**: Recharts
- **Animations**: Framer Motion
- **API Mocking**: MSW (Mock Service Worker)
- **Validation**: Zod

## Getting Started

### Prerequisites

- Node.js 18+
- npm or pnpm

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Generate API types**:
   ```bash
   npm run gen:api
   ```

3. **Set environment variables**:
   ```bash
   export NEXT_PUBLIC_API_BASE="http://localhost:8000"
   export NEXT_PUBLIC_TENANT="bigsky"
   export NEXT_PUBLIC_USE_MOCKS="true"
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

The UI will be available at `http://localhost:3000`.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE` | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_TENANT` | Default tenant ID | `bigsky` |
| `NEXT_PUBLIC_USE_MOCKS` | Enable MSW mocking | `false` |

## Tenant Switching

### Method 1: Environment Variable
```bash
export NEXT_PUBLIC_TENANT="acme"
npm run dev
```

### Method 2: URL Parameter
```
http://localhost:3000?tenant=acme
```

### Available Tenants

- **Big Sky Ag** (`bigsky`): Starter plan with limited features
- **Acme Corporation** (`acme`): Corporate plan with full features

## Mock vs Live API

### Using Mocks (Development)
```bash
export NEXT_PUBLIC_USE_MOCKS="true"
npm run dev
```

### Using Live API
```bash
export NEXT_PUBLIC_USE_MOCKS="false"
npm run dev
```

## Managed Services

The Managed Services feature allows tenants to enable/disable additional platform services:

### Starter Plan (Big Sky)
- Services are **read-only** (locked)
- Toggles are disabled with lock icons
- Shows upgrade prompts

### Corporate Plan (Acme)
- Full access to all services
- Can enable/disable services
- Real-time status updates

### Enabling Services for Big Sky

To enable Managed Services for Big Sky (for testing):

1. **Backend Override**: Update `tenants/bigsky.yaml`:
   ```yaml
   feature_flags:
     ENABLE_MANAGED_SERVICES: true
   ```

2. **Restart Backend**: Restart the FastAPI server to pick up changes

3. **Refresh UI**: The UI will automatically reflect the new permissions

## API Endpoints

The UI consumes these backend endpoints:

- `GET /branding` - Tenant branding information
- `GET /features` - Feature flags and limits
- `GET /reports/summary` - Dashboard summary data
- `GET /files` - File listing
- `POST /files` - File upload
- `GET /backups` - Backup status
- `POST /backups` - Create backup
- `GET /operations` - Recent operations
- `GET /services/catalog` - Available services
- `GET /services/status` - Service status
- `POST /services/enable` - Enable service
- `POST /services/disable` - Disable service
- `GET /auth/user` - User information
- `GET /health` - System health

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run gen:api` - Generate API types from OpenAPI spec
- `npm run test` - Run tests (when implemented)

### Project Structure

```
src/
├── app/                 # Next.js app router pages
├── components/          # React components
│   ├── ui/             # shadcn/ui components
│   └── ...             # Custom components
├── lib/                # Utilities and hooks
│   ├── api.ts          # API client
│   ├── auth.ts         # Authentication
│   ├── query.ts        # React Query hooks
│   ├── schemas.ts      # Zod schemas
│   ├── theme.ts        # Theming utilities
│   └── ws.ts           # WebSocket utilities
├── mocks/              # MSW handlers
└── types/              # Generated TypeScript types
```

### Adding New Features

1. **Create Zod schema** in `src/lib/schemas.ts`
2. **Add API client** in `src/lib/api.ts`
3. **Create React Query hook** in `src/lib/query.ts`
4. **Build UI component** in `src/components/`
5. **Add page** in `src/app/`
6. **Update MSW handlers** in `src/mocks/handlers.ts`

## Testing

### Component Testing
```bash
npm run test
```

### E2E Testing
```bash
npm run test:e2e
```

## Deployment

### Build
```bash
npm run build
```

### Start Production
```bash
npm run start
```

## Troubleshooting

### Common Issues

1. **API Types Not Generated**
   ```bash
   npm run gen:api
   ```

2. **MSW Not Working**
   - Ensure `NEXT_PUBLIC_USE_MOCKS="true"`
   - Check browser console for MSW errors

3. **Tenant Not Switching**
   - Clear browser cache
   - Check environment variables
   - Verify backend tenant configuration

4. **WebSocket Connection Failed**
   - Backend WebSocket endpoint may not be implemented
   - Mock WebSocket will be used automatically

### Debug Mode

Enable debug logging:
```bash
export NEXT_PUBLIC_DEBUG="true"
npm run dev
```

## Contributing

1. Follow the existing code structure
2. Add TypeScript types for all new features
3. Include Zod validation schemas
4. Update MSW handlers for new endpoints
5. Test with both mock and live APIs

## License

This project is part of the PaulyOps platform.
