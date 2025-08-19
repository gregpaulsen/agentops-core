import { NextRequest, NextResponse } from 'next/server'
import { audit, createLogger, requireSession } from '@paulyops/shared'
import { requireScopes } from '@paulyops/shared'

const digestHandler = async (req: NextRequest, context: any) => {
  const { session } = context
  const logger = createLogger({ orgId: session.orgId, userId: session.userId })

  const body = await req.json()
  const { days } = body

  if (!days || typeof days !== 'number' || days < 1 || days > 30) {
    return NextResponse.json(
      { error: 'Days must be a number between 1 and 30' },
      { status: 400 }
    )
  }

  // Mock digest generation
  const messageCount = Math.floor(Math.random() * 100) + 10
  const summary = `Generated digest for ${days} days with ${messageCount} messages processed.`

  // Audit the digest generation
  await audit('digest.render', {
    orgId: session.orgId,
    userId: session.userId,
    entity: 'digest',
    metadata: {
      days,
      messageCount,
      summary,
    },
  })

  logger.info({
    days,
    messageCount,
    summary,
  }, 'Digest rendered')

  return NextResponse.json({
    summary,
    messageCount,
  })
}

export const POST = requireScopes(['gmail.read'])(digestHandler)
