import { execa } from 'execa'
import { DoctorConfig } from '../types'

export class GitManager {
  private config: DoctorConfig

  constructor(config: DoctorConfig) {
    this.config = config
  }

  async createSavepoint(): Promise<string> {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
    const tagName = `doctor-savepoint-${timestamp}`

    try {
      // Check if we're in a git repo
      await execa('git', ['rev-parse', '--is-inside-work-tree'])
      
      // Create savepoint tag
      await execa('git', ['tag', tagName])
      
      return tagName
    } catch (error) {
      throw new Error(`Failed to create savepoint: ${error}`)
    }
  }

  async rollbackToSavepoint(savepoint: string): Promise<boolean> {
    if (!this.config.allowSurgical) {
      throw new Error('Surgical mode not allowed for rollback')
    }

    try {
      // Reset to savepoint
      await execa('git', ['reset', '--hard', savepoint])
      
      // Clean untracked files
      await execa('git', ['clean', '-fd'])
      
      // Reinstall dependencies
      await execa('pnpm', ['install'])
      
      return true
    } catch (error) {
      throw new Error(`Failed to rollback to savepoint ${savepoint}: ${error}`)
    }
  }

  async getCurrentBranch(): Promise<string> {
    try {
      const { stdout } = await execa('git', ['branch', '--show-current'])
      return stdout.trim()
    } catch (error) {
      return 'unknown'
    }
  }

  async getLastCommit(): Promise<string> {
    try {
      const { stdout } = await execa('git', ['rev-parse', '--short', 'HEAD'])
      return stdout.trim()
    } catch (error) {
      return 'unknown'
    }
  }
}
