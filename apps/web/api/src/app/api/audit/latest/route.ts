import { NextRequest, NextResponse } from 'next/server'
import { requireSession } from '@paulyops/shared'

export async function GET(req: NextRequest) {
  try {
    const session = await requireSession(req)
    
    // For now, return mock data since we don't have DB connection
    // In production, this would query the AuditLog table
    const mockLogs = [
      {
        id: '1',
        action: 'doctor.run',
        entity: 'system',
        timestamp: new Date().toISOString(),
        metadata: { mode: 'scan', summary: { ok: 4, warn: 1, fail: 4 } }
      },
      {
        id: '2',
        action: 'permission.allowed',
        entity: 'api',
        timestamp: new Date(Date.now() - 60000).toISOString(),
        metadata: { requiredScopes: ['gmail.read'], grantedFrom: 'read-only' }
      },
      {
        id: '3',
        action: 'digest.render',
        entity: 'digest',
        timestamp: new Date(Date.now() - 120000).toISOString(),
        metadata: { days: 7, messageCount: 45 }
      }
    ]

    return NextResponse.json({
      logs: mockLogs,
      count: mockLogs.length
    })
  } catch (error: any) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to fetch audit logs' },
      { status: 500 }
    )
  }
}
