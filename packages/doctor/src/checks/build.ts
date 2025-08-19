import { CheckResult, RepairAction } from '../types'
import { ShellRunner } from '../utils/shell'
import { DoctorConfig } from '../types'

export async function checkBuild(config: DoctorConfig): Promise<CheckResult> {
  const startTime = Date.now()
  const shell = new ShellRunner(config)

  try {
    // Run a quick build test
    const { success, output } = await shell.runSafeCommand(
      'pnpm -w build',
      'Test build process'
    )

    const duration = Date.now() - startTime

    if (success) {
      return {
        name: 'build',
        status: 'ok',
        message: 'Build process successful',
        details: { built: true },
        duration
      }
    }

    const fix: RepairAction = {
      type: 'build_fix',
      command: 'pnpm -w build',
      description: 'Rebuild project',
      risky: false
    }

    return {
      name: 'build',
      status: 'fail',
      message: 'Build process failed',
      details: { error: output },
      fix,
      duration
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    const fix: RepairAction = {
      type: 'build_fix',
      command: 'pnpm -w build',
      description: 'Rebuild project',
      risky: false
    }

    return {
      name: 'build',
      status: 'fail',
      message: `Build check failed: ${error.message}`,
      details: { error: error.message },
      fix,
      duration
    }
  }
}
