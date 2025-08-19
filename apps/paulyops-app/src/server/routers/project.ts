import { router, publicProcedure } from '../trpc'
import { z } from 'zod'
import { db } from '../db'
import { projects } from '@paulyops/db'
import { eq } from 'drizzle-orm'

export const projectRouter = router({
  list: publicProcedure.query(async () => {
    return await db.select().from(projects)
  }),
  
  create: publicProcedure
    .input(z.object({ 
      orgId: z.string().uuid(), 
      name: z.string().min(1) 
    }))
    .mutation(async ({ input }: { input: { orgId: string; name: string } }) => {
      return await db.insert(projects).values(input).returning()
    }),
    
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ input }: { input: { id: string } }) => {
      const result = await db.select().from(projects).where(eq(projects.id, input.id))
      return result[0]
    }),
})
