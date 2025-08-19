import { NextRequest, NextResponse } from 'next/server'
import { telemetry, createLogger, requireSession } from '@paulyops/shared'

export async function POST(req: NextRequest) {
  try {
    const session = await requireSession(req)
    const logger = createLogger({ orgId: session.orgId, userId: session.userId })

    const body = await req.json()
    const { type, payload } = body

    if (!type) {
      return NextResponse.json(
        { error: 'Event type is required' },
        { status: 400 }
      )
    }

    // Log telemetry event
    await telemetry(type, {
      orgId: session.orgId,
      userId: session.userId,
      payload,
    })

    const eventId = `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    logger.info({
      eventId,
      type,
      payload,
    }, 'Telemetry event logged')

    return NextResponse.json({
      id: eventId,
      status: 'logged',
    })
  } catch (error) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to log telemetry event' },
      { status: 500 }
    )
  }
}
