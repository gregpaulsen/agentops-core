import { NextRequest, NextResponse } from 'next/server'
import { requireSession } from '@paulyops/shared'
import * as fs from 'fs'
import * as path from 'path'

export async function GET(req: NextRequest) {
  try {
    // Check authentication
    await requireSession(req)
    
    const statusPath = path.join(process.cwd(), 'apps/api/public/status.json')
    
    if (fs.existsSync(statusPath)) {
      const statusData = fs.readFileSync(statusPath, 'utf8')
      const status = JSON.parse(statusData)
      
      return NextResponse.json({
        ...status,
        timestamp: new Date().toISOString()
      })
    }

    // Return default status if no status file exists
    return NextResponse.json({
      lastRun: null,
      summary: { ok: 0, warn: 0, fail: 0 },
      failingChecks: [],
      mode: 'scan',
      timestamp: new Date().toISOString()
    })
  } catch (error: any) {
    if (error instanceof Error && error.message.includes('Authentication required')) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to read status' },
      { status: 500 }
    )
  }
}
