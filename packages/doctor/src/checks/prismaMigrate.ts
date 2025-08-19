import { CheckResult, RepairAction } from '../types'
import { ShellRunner } from '../utils/shell'
import { DoctorConfig } from '../types'

export async function checkPrismaMigrate(config: DoctorConfig): Promise<CheckResult> {
  const startTime = Date.now()
  const shell = new ShellRunner(config)

  try {
    // Check migration status
    const { success, output } = await shell.runSafeCommand(
      'pnpm dlx prisma migrate status',
      'Check Prisma migration status'
    )

    const duration = Date.now() - startTime

    if (success) {
      // Check if there are pending migrations
      if (output.includes('Pending') || output.includes('not applied')) {
        const fix: RepairAction = {
          type: 'prisma_migrate',
          command: 'pnpm dlx prisma migrate deploy',
          description: 'Apply pending database migrations',
          risky: true
        }

        return {
          name: 'prismaMigrate',
          status: 'warn',
          message: 'Database has pending migrations',
          details: { status: output },
          fix,
          duration
        }
      }

      return {
        name: 'prismaMigrate',
        status: 'ok',
        message: 'Database migrations are up to date',
        details: { status: output },
        duration
      }
    }

    const fix: RepairAction = {
      type: 'prisma_migrate',
      command: 'pnpm dlx prisma migrate deploy',
      description: 'Apply database migrations',
      risky: true
    }

    return {
      name: 'prismaMigrate',
      status: 'fail',
      message: 'Failed to check migration status',
      details: { error: output },
      fix,
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    const fix: RepairAction = {
      type: 'prisma_migrate',
      command: 'pnpm dlx prisma migrate deploy',
      description: 'Apply database migrations',
      risky: true
    }

    return {
      name: 'prismaMigrate',
      status: 'fail',
      message: `Migration check failed: ${error.message}`,
      details: { error: error.message },
      fix,
      duration
    }
  }
}
