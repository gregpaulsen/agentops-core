import { NextRequest, NextResponse } from 'next/server'
import { audit, createLogger, requireSession } from '@paulyops/shared'
import { requireScopes } from '@paulyops/shared'

const inboxActionHandler = async (req: NextRequest, context: any) => {
  const { session } = context
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
}

export const POST = requireScopes(['gmail.modify'])(inboxActionHandler)
