import * as fs from 'fs'
import * as path from 'path'
import { DoctorMode, DoctorConfig, DoctorReport, CheckResult } from './types'
import { ShellRunner } from './utils/shell'
import { GitManager } from './utils/git'
import { Fixer } from './fixers'
import { logger, audit, telemetry } from '@paulyops/shared'
import { sendNotifications } from '@paulyops/shared'

// Import all checks
import { checkEnvironment } from './checks/env'
import { checkDatabase } from './checks/db'
import { checkPrismaGenerate } from './checks/prismaGenerate'
import { checkPrismaMigrate } from './checks/prismaMigrate'
import { checkDepsSync } from './checks/depsSync'
import { checkBuild } from './checks/build'
import { checkDisk } from './checks/disk'
import { checkMemoryCpu } from './checks/memoryCpu'
import { checkProviders } from './checks/providers'

export async function runDoctor(options: { mode: DoctorMode }): Promise<DoctorReport> {
  const startTime = Date.now()
  
  // Load configuration
  const config = await loadConfig()
  config.mode = options.mode

  logger.info({
    mode: config.mode,
    allowSurgical: config.allowSurgical
  }, 'Starting PaulyOps System Doctor')

  // Create savepoint if in repair or surgical mode
  let savepoint: string | undefined
  if (config.mode === 'repair' || config.mode === 'surgical') {
    const gitManager = new GitManager(config)
    try {
      savepoint = await gitManager.createSavepoint()
      logger.info({ savepoint }, 'Created git savepoint')
    } catch (error) {
      logger.warn({ error }, 'Failed to create savepoint')
    }
  }

  // Run all enabled checks
  const checks: CheckResult[] = []
  const checkFunctions = [
    { name: 'env', fn: checkEnvironment, enabled: config.checks.env },
    { name: 'db', fn: checkDatabase, enabled: config.checks.db },
    { name: 'prismaGenerate', fn: () => checkPrismaGenerate(config), enabled: config.checks.prismaGenerate },
    { name: 'prismaMigrate', fn: () => checkPrismaMigrate(config), enabled: config.checks.prismaMigrate },
    { name: 'depsSync', fn: () => checkDepsSync(config), enabled: config.checks.depsSync },
    { name: 'build', fn: () => checkBuild(config), enabled: config.checks.build },
    { name: 'disk', fn: () => checkDisk(config), enabled: config.checks.disk },
    { name: 'memoryCpu', fn: () => checkMemoryCpu(config), enabled: config.checks.memoryCpu },
    { name: 'providers', fn: checkProviders, enabled: config.checks.providers }
  ]

  for (const check of checkFunctions) {
    if (!check.enabled) continue

    try {
      const result = await check.fn()
      checks.push(result)

      // Emit telemetry for each check
      await telemetry(`doctor.check.${result.status}`, {
        orgId: 'system',
        payload: {
          check: check.name,
          status: result.status,
          duration: result.duration,
          message: result.message
        }
      })

      logger.info({
        check: check.name,
        status: result.status,
        duration: result.duration
      }, `Check completed: ${check.name}`)
    } catch (error: any) {
      const failedCheck: CheckResult = {
        name: check.name,
        status: 'fail',
        message: `Check failed: ${error.message}`,
        details: { error: error.message },
        duration: Date.now() - startTime
      }
      checks.push(failedCheck)

      logger.error({
        check: check.name,
        error: error.message
      }, `Check failed: ${check.name}`)
    }
  }

  // Execute repairs if needed
  const repairs: any[] = []
  if (config.mode === 'repair' || config.mode === 'surgical') {
    const fixer = new Fixer(config)
    
    for (const check of checks) {
      if (check.status === 'fail' && check.fix) {
        logger.info({
          check: check.name,
          fix: check.fix.type
        }, 'Executing repair')

        const success = await fixer.executeFix(check.fix)
        repairs.push({
          check: check.name,
          action: check.fix,
          success
        })

        if (success) {
          // Re-run the check to verify fix
          try {
            // Find the original check function and re-run it
            const checkFunction = checkFunctions.find(cf => cf.name === check.name)
            if (checkFunction) {
              const recheck = await checkFunction.fn()
              const originalIndex = checks.findIndex(c => c.name === check.name)
              if (originalIndex !== -1) {
                checks[originalIndex] = recheck
              }
            }
          } catch (error: any) {
            logger.warn({
              check: check.name,
              error: error.message
            }, 'Failed to re-verify check after repair')
          }
        }
      }
    }
  }

  // Calculate summary
  const summary = {
    ok: checks.filter(c => c.status === 'ok').length,
    warn: checks.filter(c => c.status === 'warn').length,
    fail: checks.filter(c => c.status === 'fail').length
  }

  const failingChecks = checks.filter(c => c.status === 'fail').map(c => c.name)
  const duration = Date.now() - startTime

  // Create report
  const report: DoctorReport = {
    timestamp: new Date().toISOString(),
    mode: config.mode,
    summary,
    checks,
    failingChecks,
    duration,
    savepoint,
    repairs
  }

  // Write status page
  await writeStatusPage(report, config.statusPage)

  // Send notifications if any checks failed
  if (summary.fail > 0) {
    await sendDoctorNotifications(report, config)
  }

  // Audit the doctor run
  await audit('doctor.run', {
    orgId: 'system',
    entity: 'system',
    metadata: {
      mode: config.mode,
      summary,
      failingChecks,
      duration,
      savepoint
    }
  })

  logger.info({
    mode: config.mode,
    summary,
    duration,
    savepoint
  }, 'PaulyOps System Doctor completed')

  return report
}

async function loadConfig(): Promise<DoctorConfig> {
  const configPath = path.join(process.cwd(), 'doctor.config.json')
  
  if (!fs.existsSync(configPath)) {
    throw new Error('doctor.config.json not found')
  }

  const configData = fs.readFileSync(configPath, 'utf8')
  const config = JSON.parse(configData)

  // Replace environment variables in config
  if (config.notifications.slackWebhook.startsWith('${') && config.notifications.slackWebhook.endsWith('}')) {
    const envVar = config.notifications.slackWebhook.slice(2, -1)
    config.notifications.slackWebhook = process.env[envVar] || ''
  }

  return config
}

async function writeStatusPage(report: DoctorReport, statusPagePath: string): Promise<void> {
  try {
    const statusData = {
      lastRun: report.timestamp,
      summary: report.summary,
      failingChecks: report.failingChecks,
      mode: report.mode
    }

    // Ensure directory exists
    const dir = path.dirname(statusPagePath)
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true })
    }

    fs.writeFileSync(statusPagePath, JSON.stringify(statusData, null, 2))
    
    logger.info({
      path: statusPagePath
    }, 'Status page updated')
  } catch (error: any) {
    logger.error({
      error: error.message,
      path: statusPagePath
    }, 'Failed to write status page')
  }
}

async function sendDoctorNotifications(report: DoctorReport, config: DoctorConfig): Promise<void> {
  if (report.summary.fail > 0) {
    try {
      const payload = {
        text: `🩺 PaulyOps Doctor: ${report.summary.fail} FAIL on ${require('os').hostname()}`,
        attachments: [{
          color: 'danger',
          fields: [
            {
              title: 'Failing Checks',
              value: report.failingChecks.join(', ') || 'None',
              short: true
            },
            {
              title: 'Mode',
              value: report.mode,
              short: true
            },
            {
              title: 'Duration',
              value: `${report.duration}ms`,
              short: true
            }
          ]
        }]
      }

      await sendNotifications(payload)
    } catch (error: any) {
      logger.error({
        error: error.message
      }, 'Failed to send doctor notifications')
    }
  }
}
