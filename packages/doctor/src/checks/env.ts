import { CheckResult, RepairAction } from '../types'

export async function checkEnvironment(): Promise<CheckResult> {
  const startTime = Date.now()
  const requiredVars = [
    'DATABASE_URL',
    'NEXTAUTH_SECRET',
    'NEXTAUTH_URL'
  ]

  const missing: string[] = []
  const present: string[] = []

  for (const varName of requiredVars) {
    if (process.env[varName]) {
      present.push(varName)
    } else {
      missing.push(varName)
    }
  }

  const duration = Date.now() - startTime

  if (missing.length === 0) {
    return {
      name: 'env',
      status: 'ok',
      message: `All required environment variables present (${present.length})`,
      details: { present },
      duration
    }
  }

  const fix: RepairAction = {
    type: 'env_setup',
    description: `Set missing environment variables: ${missing.join(', ')}`,
    risky: false
  }

  return {
    name: 'env',
    status: 'fail',
    message: `Missing required environment variables: ${missing.join(', ')}`,
    details: { missing, present },
    fix,
    duration
  }
}
