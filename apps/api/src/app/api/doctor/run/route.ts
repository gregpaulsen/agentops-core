import { NextRequest, NextResponse } from 'next/server'
import { requireSession, createLogger } from '@paulyops/shared'
import { runDoctor } from '@paulyops/doctor'

export async function POST(req: NextRequest) {
  try {
    const session = await requireSession(req)
    const logger = createLogger({ orgId: session.orgId, userId: session.userId })

    const body = await req.json()
    const { mode = 'scan' } = body

    if (!['scan', 'repair', 'surgical'].includes(mode)) {
      return NextResponse.json(
        { error: 'Invalid mode. Must be scan, repair, or surgical' },
        { status: 400 }
      )
    }

    // Check if surgical mode is allowed
    if (mode === 'surgical') {
      // In a real implementation, you'd check the config
      const allowSurgical = false // This should come from config
      if (!allowSurgical) {
        return NextResponse.json(
          { error: 'Surgical mode not allowed' },
          { status: 403 }
        )
      }
    }

    logger.info({
      mode,
      userId: session.userId
    }, 'Starting doctor run via API')

    // Run the doctor
    const report = await runDoctor({ mode })

    logger.info({
      mode,
      summary: report.summary,
      duration: report.duration
    }, 'Doctor run completed via API')

    return NextResponse.json({
      success: true,
      report,
      jobId: `doctor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    })
  } catch (error: any) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: `Doctor run failed: ${error.message}` },
      { status: 500 }
    )
  }
}
