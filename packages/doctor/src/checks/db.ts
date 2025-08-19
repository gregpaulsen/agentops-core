import { CheckResult, RepairAction } from '../types'
import { prisma } from '@paulyops/shared'

export async function checkDatabase(): Promise<CheckResult> {
  const startTime = Date.now()

  try {
    // Test database connectivity
    await prisma.$queryRaw`SELECT 1`
    
    const duration = Date.now() - startTime
    
    return {
      name: 'db',
      status: 'ok',
      message: 'Database connection successful',
      details: { connected: true },
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime
    
    const fix: RepairAction = {
      type: 'db_connect',
      description: 'Check DATABASE_URL and database server status',
      risky: false
    }

    return {
      name: 'db',
      status: 'fail',
      message: `Database connection failed: ${error.message}`,
      details: { error: error.message },
      fix,
      duration
    }
  }
}
