import { betterAuth } from 'better-auth'
import { db } from '@paulyops/db'
import { users, organizations, memberships } from '@paulyops/db'
import { eq } from 'drizzle-orm'

export const auth = betterAuth({
  database: {
    type: 'custom',
    adapter: {
      // User management
      async createUser(data) {
        const [user] = await db.insert(users).values({
          email: data.email,
          name: data.name,
          image: data.image,
        }).returning()
        return user
      },
      async getUser(userId) {
        const [user] = await db.select().from(users).where(eq(users.id, userId))
        return user || null
      },
      async getUserByEmail(email) {
        const [user] = await db.select().from(users).where(eq(users.email, email))
        return user || null
      },
      async updateUser(userId, data) {
        const [user] = await db.update(users)
          .set(data)
          .where(eq(users.id, userId))
          .returning()
        return user
      },
      async deleteUser(userId) {
        await db.delete(users).where(eq(users.id, userId))
      },

      // Session management
      async createSession(data) {
        // Sessions are handled by Better Auth internally
        return data
      },
      async getSession(sessionId) {
        // Sessions are handled by Better Auth internally
        return null
      },
      async updateSession(sessionId, data) {
        // Sessions are handled by Better Auth internally
        return data
      },
      async deleteSession(sessionId) {
        // Sessions are handled by Better Auth internally
      },

      // Account management
      async createAccount(data) {
        // Accounts are handled by Better Auth internally
        return data
      },
      async getAccount(provider, providerAccountId) {
        // Accounts are handled by Better Auth internally
        return null
      },
      async updateAccount(provider, providerAccountId, data) {
        // Accounts are handled by Better Auth internally
        return data
      },
      async deleteAccount(provider, providerAccountId) {
        // Accounts are handled by Better Auth internally
      },
    },
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  providers: {
    google: {
      type: 'oauth',
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    microsoft: {
      type: 'oauth',
      clientId: process.env.MICROSOFT_CLIENT_ID!,
      clientSecret: process.env.MICROSOFT_CLIENT_SECRET!,
    },
  },
  callbacks: {
    async signIn({ user, account, profile }) {
      // Ensure user has access to at least one organization
      const userMemberships = await db.select()
        .from(memberships)
        .where(eq(memberships.userId, user.id))
      
      if (userMemberships.length === 0) {
        // Create default organization for new users
        const [org] = await db.insert(organizations).values({
          name: `${user.name || user.email}'s Organization`,
          slug: `org-${user.id}`,
        }).returning()
        
        await db.insert(memberships).values({
          userId: user.id,
          organizationId: org.id,
          role: 'owner',
        })
      }
      
      return true
    },
  },
})

// Helper functions
export const currentUser = auth.currentUser
export const requireAuth = auth.requireAuth

export function requireRole(role: 'owner' | 'admin' | 'member') {
  return async (req: Request) => {
    const user = await currentUser(req)
    if (!user) throw new Error('Authentication required')
    
    const userMemberships = await db.select()
      .from(memberships)
      .where(eq(memberships.userId, user.id))
    
    const hasRole = userMemberships.some(m => m.role === role || m.role === 'owner')
    if (!hasRole) throw new Error(`Role ${role} required`)
    
    return user
  }
}

export function requireAdmin() {
  return requireRole('admin')
}

export function requireOwner() {
  return requireRole('owner')
}

// Export auth for use in Next.js
export { auth as default }
