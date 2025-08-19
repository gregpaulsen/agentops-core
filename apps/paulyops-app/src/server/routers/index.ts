import { router } from '../trpc'
import { projectRouter } from './project'
import { resourcesRouter } from './resources'

export const appRouter = router({
  projectRouter: projectRouter,
  resourcesRouter: resourcesRouter,
})

export type AppRouter = typeof appRouter
