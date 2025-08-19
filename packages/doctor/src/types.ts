export type DoctorMode = 'scan' | 'repair' | 'surgical'

export type CheckStatus = 'ok' | 'warn' | 'fail'

export interface CheckResult {
  name: string
  status: CheckStatus
  message: string
  details?: Record<string, any>
  fix?: RepairAction
  duration?: number
}

export interface RepairAction {
  type: string
  command?: string
  description: string
  risky?: boolean
}

export interface RepairResult {
  check: string
  action: RepairAction
  success: boolean
}

export interface DoctorReport {
  timestamp: string
  mode: DoctorMode
  summary: {
    ok: number
    warn: number
    fail: number
  }
  checks: CheckResult[]
  failingChecks: string[]
  duration: number
  savepoint?: string
  repairs: RepairResult[]
}

export interface DoctorConfig {
  mode: DoctorMode
  allowSurgical: boolean
  checks: Record<string, boolean>
  thresholds: {
    diskFreePctMin: number
    memFreePctMin: number
    cpuLoadMax: number
  }
  notifications: {
    slackWebhook: string
    discordWebhook: string
  }
  statusPage: string
  whitelistCommands: string[]
}

export interface SystemMetrics {
  diskFreePercent: number
  memoryFreePercent: number
  cpuLoad: number
  uptime: number
}
