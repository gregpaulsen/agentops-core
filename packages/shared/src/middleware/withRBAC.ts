import { requireRole } from '../lib/auth'

// Simplified middleware without Next.js dependencies
export function withRBAC(allowedRoles: string[]) {
  return function(handler: (req: any, context: { session: any }) => Promise<any>) {
    return async (req: any) => {
      try {
        const session = await requireRole(allowedRoles)(req)
        return handler(req, { session })
      } catch (error) {
        if (error instanceof Error && error.message.includes('Insufficient permissions')) {
          return {
            status: 403,
            json: () => ({ error: 'Insufficient permissions' })
          }
        }
        return {
          status: 401,
          json: () => ({ error: 'Authentication required' })
        }
      }
    }
  }
}

export const withAdmin = withRBAC(['admin', 'owner'])
export const withOwner = withRBAC(['owner'])
