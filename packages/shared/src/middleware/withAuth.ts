import { requireSession } from '../lib/auth'

// Simplified middleware without Next.js dependencies
export function withAuth(handler: (req: any, context: { session: any }) => Promise<any>) {
  return async (req: any) => {
    try {
      const session = await requireSession(req)
      return handler(req, { session })
    } catch (error) {
      return {
        status: 401,
        json: () => ({ error: 'Authentication required' })
      }
    }
  }
}
