import { drizzle } from 'drizzle-orm/node-postgres'
import { Pool } from 'pg'
import * as schema from './schema'

// Database client
const pool = new Pool({
  connectionString: process.env.NEON_DATABASE_URL || process.env.DATABASE_URL,
})

export const db = drizzle(pool, { schema })

// Export all schemas and types
export * from './schema'

// Export the database client
export { db as default }
