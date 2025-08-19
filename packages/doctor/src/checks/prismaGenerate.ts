import { CheckResult, RepairAction } from '../types'
import { ShellRunner } from '../utils/shell'
import { DoctorConfig } from '../types'

export async function checkPrismaGenerate(config: DoctorConfig): Promise<CheckResult> {
  const startTime = Date.now()
  const shell = new ShellRunner(config)

  try {
    // Check if Prisma client exists and is up to date
    const { success, output } = await shell.runSafeCommand(
      'pnpm dlx prisma generate',
      'Generate Prisma client'
    )

    const duration = Date.now() - startTime

    if (success) {
      return {
        name: 'prismaGenerate',
        status: 'ok',
        message: 'Prisma client is up to date',
        details: { generated: true },
        duration
      }
    }

    const fix: RepairAction = {
      type: 'prisma_generate',
      command: 'pnpm dlx prisma generate',
      description: 'Regenerate Prisma client',
      risky: false
    }

    return {
      name: 'prismaGenerate',
      status: 'fail',
      message: 'Prisma client needs regeneration',
      details: { error: output },
      fix,
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    const fix: RepairAction = {
      type: 'prisma_generate',
      command: 'pnpm dlx prisma generate',
      description: 'Regenerate Prisma client',
      risky: false
    }

    return {
      name: 'prismaGenerate',
      status: 'fail',
      message: `Prisma generate check failed: ${error.message}`,
      details: { error: error.message },
      fix,
      duration
    }
  }
}
