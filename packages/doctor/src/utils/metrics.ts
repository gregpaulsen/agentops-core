import { execa } from 'execa'
import * as os from 'os'
import { SystemMetrics } from '../types'

export class MetricsCollector {
  async getSystemMetrics(): Promise<SystemMetrics> {
    const [diskMetrics, memoryMetrics, cpuMetrics, uptime] = await Promise.all([
      this.getDiskMetrics(),
      this.getMemoryMetrics(),
      this.getCpuMetrics(),
      this.getUptime()
    ])

    return {
      diskFreePercent: diskMetrics.freePercent,
      memoryFreePercent: memoryMetrics.freePercent,
      cpuLoad: cpuMetrics.load,
      uptime
    }
  }

  private async getDiskMetrics(): Promise<{ freePercent: number }> {
    try {
      const { stdout } = await execa('df', ['-k', '.'])
      const lines = stdout.trim().split('\n')
      const dataLine = lines[1] // Skip header
      const parts = dataLine.split(/\s+/)
      
      const total = parseInt(parts[1])
      const used = parseInt(parts[2])
      const available = parseInt(parts[3])
      
      const freePercent = Math.round((available / total) * 100)
      
      return { freePercent }
    } catch (error) {
      // Fallback to Node.js os module
      const total = os.totalmem()
      const free = os.freemem()
      const freePercent = Math.round((free / total) * 100)
      
      return { freePercent }
    }
  }

  private async getMemoryMetrics(): Promise<{ freePercent: number }> {
    const total = os.totalmem()
    const free = os.freemem()
    const freePercent = Math.round((free / total) * 100)
    
    return { freePercent }
  }

  private async getCpuMetrics(): Promise<{ load: number }> {
    try {
      const { stdout } = await execa('uptime')
      // Parse load average from uptime output
      const loadMatch = stdout.match(/load average: ([\d.]+)/)
      const load = loadMatch ? parseFloat(loadMatch[1]) : 0
      
      return { load }
    } catch (error) {
      // Fallback to Node.js os module
      const load = os.loadavg()[0] || 0
      return { load }
    }
  }

  private async getUptime(): Promise<number> {
    try {
      const { stdout } = await execa('uptime')
      const uptimeMatch = stdout.match(/up\s+([^,]+)/)
      if (uptimeMatch) {
        // Simple parsing for common formats
        const uptimeStr = uptimeMatch[1]
        if (uptimeStr.includes('days')) {
          const days = parseInt(uptimeStr.match(/(\d+)\s*days?/)?.[1] || '0')
          return days * 24 * 60 * 60
        }
      }
      return os.uptime()
    } catch (error) {
      return os.uptime()
    }
  }
}
