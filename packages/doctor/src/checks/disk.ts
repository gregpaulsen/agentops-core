import { CheckResult, RepairAction } from '../types'
import { MetricsCollector } from '../utils/metrics'
import { DoctorConfig } from '../types'

export async function checkDisk(config: DoctorConfig): Promise<CheckResult> {
  const startTime = Date.now()
  const metrics = new MetricsCollector()

  try {
    const systemMetrics = await metrics.getSystemMetrics()
    const duration = Date.now() - startTime

    const threshold = config.thresholds.diskFreePctMin
    const freePercent = systemMetrics.diskFreePercent

    if (freePercent >= threshold) {
      return {
        name: 'disk',
        status: 'ok',
        message: `Disk space adequate (${freePercent}% free)`,
        details: { freePercent, threshold },
        duration
      }
    }

    if (freePercent >= threshold * 0.5) {
      const fix: RepairAction = {
        type: 'disk_cleanup',
        description: `Low disk space: ${freePercent}% free (threshold: ${threshold}%)`,
        risky: false
      }

      return {
        name: 'disk',
        status: 'warn',
        message: `Low disk space: ${freePercent}% free`,
        details: { freePercent, threshold },
        fix,
        duration
      }
    }

    const fix: RepairAction = {
      type: 'disk_cleanup',
      description: `Critical disk space: ${freePercent}% free (threshold: ${threshold}%)`,
      risky: true
    }

    return {
      name: 'disk',
      status: 'fail',
      message: `Critical disk space: ${freePercent}% free`,
      details: { freePercent, threshold },
      fix,
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    return {
      name: 'disk',
      status: 'fail',
      message: `Disk check failed: ${error.message}`,
      details: { error: error.message },
      duration
    }
  }
}
