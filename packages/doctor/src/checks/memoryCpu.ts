import { CheckResult, RepairAction } from '../types'
import { MetricsCollector } from '../utils/metrics'
import { DoctorConfig } from '../types'

export async function checkMemoryCpu(config: DoctorConfig): Promise<CheckResult> {
  const startTime = Date.now()
  const metrics = new MetricsCollector()

  try {
    const systemMetrics = await metrics.getSystemMetrics()
    const duration = Date.now() - startTime

    const memThreshold = config.thresholds.memFreePctMin
    const cpuThreshold = config.thresholds.cpuLoadMax
    const memFreePercent = systemMetrics.memoryFreePercent
    const cpuLoad = systemMetrics.cpuLoad

    const memOk = memFreePercent >= memThreshold
    const cpuOk = cpuLoad <= cpuThreshold

    if (memOk && cpuOk) {
      return {
        name: 'memoryCpu',
        status: 'ok',
        message: `Memory and CPU healthy (${memFreePercent}% mem free, ${cpuLoad} CPU load)`,
        details: { memFreePercent, cpuLoad, memThreshold, cpuThreshold },
        duration
      }
    }

    const issues: string[] = []
    if (!memOk) issues.push(`Low memory: ${memFreePercent}% free`)
    if (!cpuOk) issues.push(`High CPU: ${cpuLoad} load`)

    const fix: RepairAction = {
      type: 'system_optimize',
      description: `System resource issues: ${issues.join(', ')}`,
      risky: false
    }

    const status = (!memOk && memFreePercent < memThreshold * 0.5) || (!cpuOk && cpuLoad > cpuThreshold * 2) ? 'fail' : 'warn'

    return {
      name: 'memoryCpu',
      status,
      message: `System resource issues: ${issues.join(', ')}`,
      details: { memFreePercent, cpuLoad, memThreshold, cpuThreshold },
      fix,
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    return {
      name: 'memoryCpu',
      status: 'fail',
      message: `Memory/CPU check failed: ${error.message}`,
      details: { error: error.message },
      duration
    }
  }
}
