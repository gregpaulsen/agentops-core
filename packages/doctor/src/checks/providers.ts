import { CheckResult, RepairAction } from '../types'
import { currentProvider, fallbackProvider } from '@paulyops/shared'

export async function checkProviders(): Promise<CheckResult> {
  const startTime = Date.now()

  try {
    // Simulate provider health checks
    const primaryProvider = currentProvider()
    const secondaryProvider = fallbackProvider()

    // Mock provider health simulation
    const primaryHealthy = Math.random() > 0.2 // 80% healthy
    const secondaryHealthy = Math.random() > 0.3 // 70% healthy

    const duration = Date.now() - startTime

    if (primaryHealthy) {
      return {
        name: 'providers',
        status: 'ok',
        message: `Primary provider healthy: ${primaryProvider}`,
        details: { primaryProvider, secondaryProvider, primaryHealthy, secondaryHealthy },
        duration
      }
    }

    if (secondaryHealthy) {
      const fix: RepairAction = {
        type: 'provider_fallback',
        description: `Primary provider down, using fallback: ${secondaryProvider}`,
        risky: false
      }

      return {
        name: 'providers',
        status: 'warn',
        message: `Using fallback provider: ${secondaryProvider}`,
        details: { primaryProvider, secondaryProvider, primaryHealthy, secondaryHealthy },
        fix,
        duration
      }
    }

    const fix: RepairAction = {
      type: 'provider_emergency',
      description: 'All providers down - emergency mode',
      risky: true
    }

    return {
      name: 'providers',
      status: 'fail',
      message: 'All external providers down',
      details: { primaryProvider, secondaryProvider, primaryHealthy, secondaryHealthy },
      fix,
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    return {
      name: 'providers',
      status: 'fail',
      message: `Provider check failed: ${error.message}`,
      details: { error: error.message },
      duration
    }
  }
}
