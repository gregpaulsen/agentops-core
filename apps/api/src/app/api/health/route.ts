import { NextResponse } from 'next/server'
import { prisma } from '@paulyops/shared'

export async function GET() {
  const time = new Date().toISOString()
  
  // Check database connectivity
  let dbStatus: 'up' | 'down' = 'down'
  try {
    await prisma.$queryRaw`SELECT 1`
    dbStatus = 'up'
  } catch (error) {
    console.error('Database health check failed:', error)
  }

  return NextResponse.json({
    ok: true,
    time,
    db: dbStatus,
  })
}
