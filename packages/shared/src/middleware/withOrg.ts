import { requireSession } from '../lib/auth'

// Simplified middleware without Next.js dependencies
export function withOrg(handler: (req: any, context: { session: any, orgId: string }) => Promise<any>) {
  return async (req: any) => {
    try {
      const session = await requireSession(req)
      
      if (!session.orgId) {
        return {
          status: 400,
          json: () => ({ error: 'Organization context required' })
        }
      }
      
      return handler(req, { session, orgId: session.orgId })
    } catch (error) {
      return {
        status: 401,
        json: () => ({ error: 'Authentication required' })
      }
    }
  }
}
