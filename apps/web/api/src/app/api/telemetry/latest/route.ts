import { NextRequest, NextResponse } from 'next/server'
import { requireSession } from '@paulyops/shared'

export async function GET(req: NextRequest) {
  try {
    const session = await requireSession(req)
    
    // For now, return mock data since we don't have DB connection
    // In production, this would query the TelemetryEvent table
    const mockEvents = [
      {
        id: '1',
        type: 'doctor.check.fail',
        timestamp: new Date().toISOString(),
        payload: { check: 'env', status: 'fail', message: 'Missing environment variables' }
      },
      {
        id: '2',
        type: 'doctor.check.ok',
        timestamp: new Date(Date.now() - 30000).toISOString(),
        payload: { check: 'build', status: 'ok', message: 'Build process successful' }
      },
      {
        id: '3',
        type: 'doctor.check.warn',
        timestamp: new Date(Date.now() - 60000).toISOString(),
        payload: { check: 'memoryCpu', status: 'warn', message: 'Low memory: 8% free' }
      }
    ]

    return NextResponse.json({
      events: mockEvents,
      count: mockEvents.length
    })
  } catch (error: any) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to fetch telemetry events' },
      { status: 500 }
    )
  }
}
