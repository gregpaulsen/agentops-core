import { NextRequest, NextResponse } from 'next/server'
import { telemetry, createLogger, requireSession, runWithRetry, currentProvider, fallbackProvider } from '@paulyops/shared'

export async function POST(req: NextRequest) {
  try {
    const session = await requireSession(req)
    const logger = createLogger({ orgId: session.orgId, userId: session.userId })

    const body = await req.json()
    const { source, acres } = body

    if (!source || !['upload', 'gdrive'].includes(source)) {
      return NextResponse.json(
        { error: 'Valid source (upload or gdrive) is required' },
        { status: 400 }
      )
    }

    const jobId = `ndvi_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    // Simulate job creation with retry policy
    const createJob = async (provider: string) => {
      // Simulate potential failure
      if (Math.random() < 0.3) {
        throw new Error(`Provider ${provider} temporarily unavailable`)
      }
      
      return {
        jobId,
        status: 'pending' as const,
        retryCount: 0,
        provider,
      }
    }

    let result
    try {
      // First attempt with current provider
      result = await runWithRetry(
        () => createJob(currentProvider()),
        {
          retries: 1,
          backoffMs: 1000,
          onRetry: (attempt, error) => {
            logger.warn({
              attempt,
              error: error.message,
              provider: currentProvider(),
            }, 'NDVI job creation retry')
          },
        }
      )
    } catch (error) {
      // Fallback to secondary provider
      logger.info({
        originalProvider: currentProvider(),
        fallbackProvider: fallbackProvider(),
      }, 'Falling back to secondary provider')
      
      result = await runWithRetry(
        () => createJob(fallbackProvider()),
        {
          retries: 1,
          backoffMs: 2000,
          onRetry: (attempt, error) => {
            logger.warn({
              attempt,
              error: error.message,
              provider: fallbackProvider(),
            }, 'NDVI job creation fallback retry')
          },
        }
      )
    }

    // Log telemetry for job creation
    await telemetry('ndvi.job.created', {
      orgId: session.orgId,
      userId: session.userId,
      payload: {
        jobId,
        source,
        acres,
        provider: result.provider,
      },
    })

    logger.info({
      jobId,
      source,
      acres,
      provider: result.provider,
    }, 'NDVI job created')

    return NextResponse.json(result)
  } catch (error) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to create NDVI job' },
      { status: 500 }
    )
  }
}
