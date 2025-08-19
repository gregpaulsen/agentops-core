import { NextRequest, NextResponse } from 'next/server'
import { audit, createLogger, requireSession } from '@paulyops/shared'

export async function POST(req: NextRequest) {
  try {
    const session = await requireSession(req)
    const logger = createLogger({ orgId: session.orgId, userId: session.userId })

    const body = await req.json()
    const { message, severity, context: incidentContext } = body

    if (!message || !severity) {
      return NextResponse.json(
        { error: 'Message and severity are required' },
        { status: 400 }
      )
    }

    if (!['low', 'medium', 'high', 'critical'].includes(severity)) {
      return NextResponse.json(
        { error: 'Invalid severity level' },
        { status: 400 }
      )
    }

    const incidentId = `incident_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    // Log the incident
    await audit('incident.report', {
      orgId: session.orgId,
      userId: session.userId,
      entity: 'incident',
      entityId: incidentId,
      metadata: {
        message,
        severity,
        context: incidentContext,
      },
    })

    logger.info({
      incidentId,
      message,
      severity,
      context: incidentContext,
    }, 'Incident reported')

    return NextResponse.json({
      id: incidentId,
      status: 'reported',
    })
  } catch (error) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to report incident' },
      { status: 500 }
    )
  }
}
