import { getServerSession } from 'next-auth'
import { z } from 'zod'

// Type-safe request interface
export interface AuthRequest {
  headers: {
    get(name: string): string | null
  }
}

export interface Session {
  userId: string
  orgId: string
  role: string
  email: string
}

export interface AuthContext {
  session: Session
  request: AuthRequest
}

const sessionSchema = z.object({
  userId: z.string(),
  orgId: z.string(),
  role: z.enum(['user', 'admin', 'owner']),
  email: z.string().email(),
})

export async function getSession(request?: AuthRequest): Promise<Session | null> {
  try {
    // In a real implementation, this would use NextAuth session
    // For now, we'll simulate with headers for development
    if (request) {
      const authHeader = request.headers.get('authorization')
      if (authHeader?.startsWith('Bearer ')) {
        // Mock session for development
        return {
          userId: 'user_123',
          orgId: 'org_456',
          role: 'admin',
          email: 'admin@paulyops.com',
        }
      }
    }
    
    // Fallback to NextAuth session
    const session = await getServerSession()
    if (!session?.user) return null
    
    // Type-safe session parsing
    const user = session.user as any
    return sessionSchema.parse({
      userId: user.id || 'unknown',
      orgId: user.orgId || 'unknown',
      role: user.role || 'user',
      email: user.email || 'unknown@example.com',
    })
  } catch (error) {
    console.error('Session validation failed:', error)
    return null
  }
}

export async function requireSession(request?: AuthRequest): Promise<Session> {
  const session = await getSession(request)
  if (!session) {
    throw new Error('Authentication required')
  }
  return session
}

export function requireRole(allowedRoles: string[]) {
  return async (request?: AuthRequest): Promise<Session> => {
    const session = await requireSession(request)
    if (!allowedRoles.includes(session.role)) {
      throw new Error(`Insufficient permissions. Required roles: ${allowedRoles.join(', ')}`)
    }
    return session
  }
}

export const requireAdmin = requireRole(['admin', 'owner'])
export const requireOwner = requireRole(['owner'])
