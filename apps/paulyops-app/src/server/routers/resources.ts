import { router, publicProcedure } from '../trpc'
import { z } from 'zod'
import { searchGuides, searchTutorials, searchBestPractices } from '../youtube'

export const resourcesRouter = router({
  youtubeGuides: publicProcedure
    .input(z.object({ query: z.string().min(2) }))
    .query(async ({ input }) => {
      return await searchGuides(input.query)
    }),
    
  tutorials: publicProcedure
    .input(z.object({ topic: z.string().min(2) }))
    .query(async ({ input }) => {
      return await searchTutorials(input.topic)
    }),
    
  bestPractices: publicProcedure
    .input(z.object({ domain: z.string().min(2) }))
    .query(async ({ input }) => {
      return await searchBestPractices(input.domain)
    }),
})
