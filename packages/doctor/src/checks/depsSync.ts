import { CheckResult, RepairAction } from '../types'
import { ShellRunner } from '../utils/shell'
import { DoctorConfig } from '../types'
import * as fs from 'fs'
import * as path from 'path'

export async function checkDepsSync(config: DoctorConfig): Promise<CheckResult> {
  const startTime = Date.now()
  const shell = new ShellRunner(config)

  try {
    // Check if node_modules exists and is recent
    const nodeModulesPath = path.join(process.cwd(), 'node_modules')
    const pnpmLockPath = path.join(process.cwd(), 'pnpm-lock.yaml')

    if (!fs.existsSync(nodeModulesPath)) {
      const fix: RepairAction = {
        type: 'deps_install',
        command: 'pnpm -w install',
        description: 'Install dependencies',
        risky: false
      }

      return {
        name: 'depsSync',
        status: 'fail',
        message: 'node_modules directory missing',
        details: { missing: 'node_modules' },
        fix,
        duration: Date.now() - startTime
      }
    }

    // Check if lockfile is newer than node_modules
    const lockStats = fs.statSync(pnpmLockPath)
    const nodeModulesStats = fs.statSync(nodeModulesPath)

    if (lockStats.mtime > nodeModulesStats.mtime) {
      const fix: RepairAction = {
        type: 'deps_install',
        command: 'pnpm -w install',
        description: 'Sync dependencies with lockfile',
        risky: false
      }

      return {
        name: 'depsSync',
        status: 'warn',
        message: 'Dependencies out of sync with lockfile',
        details: { 
          lockfileModified: lockStats.mtime,
          nodeModulesModified: nodeModulesStats.mtime
        },
        fix,
        duration: Date.now() - startTime
      }
    }

    return {
      name: 'depsSync',
      status: 'ok',
      message: 'Dependencies are in sync',
      details: { synced: true },
      duration: Date.now() - startTime
    }
  } catch (error: any) {
    const duration = Date.now() - startTime

    const fix: RepairAction = {
      type: 'deps_install',
      command: 'pnpm -w install',
      description: 'Reinstall dependencies',
      risky: false
    }

    return {
      name: 'depsSync',
      status: 'fail',
      message: `Dependency check failed: ${error.message}`,
      details: { error: error.message },
      fix,
      duration
    }
  }
}
