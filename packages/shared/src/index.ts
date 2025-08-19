// Database
export { prisma } from './lib/db'

// Authentication
export { 
  getSession, 
  requireSession, 
  requireRole, 
  requireAdmin, 
  requireOwner,
  type Session,
  type AuthRequest
} from './lib/auth'

// Middleware
export { withAuth } from './middleware/withAuth'
export { withOrg } from './middleware/withOrg'
export { withRBAC, withAdmin, withOwner } from './middleware/withRBAC'

// Logging
export { 
  logger, 
  createLogger, 
  audit, 
  telemetry, 
  getRequestId 
} from './lib/logger'

// Utilities
export { runWithRetry, type RetryOptions } from './lib/retry'
export { 
  currentProvider, 
  fallbackProvider, 
  getAvailableProviders,
  type ProviderType 
} from './lib/providers'

// Permissions
export * from './permissions/manifest'
export * from './permissions/scopes'
export { requireScopes } from './middleware/withPermissions'

// Notifications
export * from './lib/notify'
