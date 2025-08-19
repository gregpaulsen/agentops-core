import { RepairAction, DoctorConfig } from '../types'
import { ShellRunner } from '../utils/shell'
import { logger, audit } from '@paulyops/shared'

export class Fixer {
  private config: DoctorConfig
  private shell: ShellRunner

  constructor(config: DoctorConfig) {
    this.config = config
    this.shell = new ShellRunner(config)
  }

  async executeFix(action: RepairAction, orgId: string = 'system'): Promise<boolean> {
    const startTime = Date.now()

    try {
      logger.info({
        action: action.type,
        description: action.description,
        risky: action.risky
      }, 'Executing repair action')

      // Audit the repair attempt
      await audit('doctor.repair', {
        orgId,
        entity: 'system',
        metadata: {
          check: action.type,
          action: action.description,
          risky: action.risky,
          command: action.command
        }
      })

      let success = false

      switch (action.type) {
        case 'prisma_generate':
          success = await this.fixPrismaGenerate()
          break
        case 'prisma_migrate':
          success = await this.fixPrismaMigrate()
          break
        case 'deps_install':
          success = await this.fixDepsInstall()
          break
        case 'build_fix':
          success = await this.fixBuild()
          break
        case 'env_setup':
          success = await this.fixEnvSetup(action)
          break
        case 'db_connect':
          success = await this.fixDbConnect()
          break
        case 'disk_cleanup':
          success = await this.fixDiskCleanup()
          break
        case 'system_optimize':
          success = await this.fixSystemOptimize()
          break
        case 'provider_fallback':
          success = await this.fixProviderFallback()
          break
        case 'provider_emergency':
          success = await this.fixProviderEmergency()
          break
        default:
          logger.warn({ action: action.type }, 'Unknown repair action type')
          return false
      }

      const duration = Date.now() - startTime

      // Audit the repair result
      await audit('doctor.repair.result', {
        orgId,
        entity: 'system',
        metadata: {
          check: action.type,
          action: action.description,
          outcome: success ? 'success' : 'failed',
          duration
        }
      })

      if (success) {
        logger.info({
          action: action.type,
          duration
        }, 'Repair action completed successfully')
      } else {
        logger.error({
          action: action.type,
          duration
        }, 'Repair action failed')
      }

      return success
    } catch (error: any) {
      logger.error({
        action: action.type,
        error: error.message
      }, 'Repair action threw error')

      return false
    }
  }

  private async fixPrismaGenerate(): Promise<boolean> {
    const { success } = await this.shell.runSafeCommand(
      'pnpm dlx prisma generate',
      'Generate Prisma client'
    )
    return success
  }

  private async fixPrismaMigrate(): Promise<boolean> {
    const { success } = await this.shell.runSafeCommand(
      'pnpm dlx prisma migrate deploy',
      'Apply database migrations'
    )
    return success
  }

  private async fixDepsInstall(): Promise<boolean> {
    const { success } = await this.shell.runSafeCommand(
      'pnpm -w install',
      'Install dependencies'
    )
    return success
  }

  private async fixBuild(): Promise<boolean> {
    const { success } = await this.shell.runSafeCommand(
      'pnpm -w build',
      'Rebuild project'
    )
    return success
  }

  private async fixEnvSetup(action: RepairAction): Promise<boolean> {
    // Environment setup requires manual intervention
    logger.warn({
      action: action.type,
      description: action.description
    }, 'Environment setup requires manual intervention')
    return false
  }

  private async fixDbConnect(): Promise<boolean> {
    // Database connection issues require manual intervention
    logger.warn({
      action: 'db_connect'
    }, 'Database connection issues require manual intervention')
    return false
  }

  private async fixDiskCleanup(): Promise<boolean> {
    // Disk cleanup requires manual intervention
    logger.warn({
      action: 'disk_cleanup'
    }, 'Disk cleanup requires manual intervention')
    return false
  }

  private async fixSystemOptimize(): Promise<boolean> {
    // System optimization requires manual intervention
    logger.warn({
      action: 'system_optimize'
    }, 'System optimization requires manual intervention')
    return false
  }

  private async fixProviderFallback(): Promise<boolean> {
    // Provider fallback is handled automatically
    logger.info({
      action: 'provider_fallback'
    }, 'Provider fallback handled automatically')
    return true
  }

  private async fixProviderEmergency(): Promise<boolean> {
    // Provider emergency requires manual intervention
    logger.error({
      action: 'provider_emergency'
    }, 'Provider emergency requires manual intervention')
    return false
  }
}
