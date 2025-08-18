import { NextRequest, NextResponse } from 'next/server'
import { audit, createLogger, requireSession } from '@paulyops/shared'

export async function POST(req: NextRequest) {
  try {
    const session = await requireSession(req)
    const logger = createLogger({ orgId: session.orgId, userId: session.userId })

    const body = await req.json()
    const { action, messageIds } = body

    if (!action || !messageIds || !Array.isArray(messageIds)) {
      return NextResponse.json(
        { error: 'Action and messageIds array are required' },
        { status: 400 }
      )
    }

    if (!['archive', 'route', 'snooze'].includes(action)) {
      return NextResponse.json(
        { error: 'Invalid action' },
        { status: 400 }
      )
    }

    if (messageIds.length === 0) {
      return NextResponse.json(
        { error: 'At least one message ID is required' },
        { status: 400 }
      )
    }

    // Mock action processing
    const processed = messageIds.length

    // Audit the inbox action
    await audit('inbox.action', {
      orgId: session.orgId,
      userId: session.userId,
      entity: 'inbox',
      metadata: {
        action,
        messageIds,
        processed,
      },
    })

    logger.info({
      action,
      messageIds,
      processed,
    }, 'Inbox action completed')

    return NextResponse.json({
      processed,
      status: 'completed',
    })
  } catch (error) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to process inbox action' },
      { status: 500 }
    )
  }
}
