import { execa } from 'execa'
import { DoctorConfig } from '../types'

export class ShellRunner {
  private config: DoctorConfig

  constructor(config: DoctorConfig) {
    this.config = config
  }

  async runCommand(command: string, timeout: number = 120000): Promise<{ stdout: string; stderr: string }> {
    // Validate command is in whitelist
    if (!this.isCommandAllowed(command)) {
      throw new Error(`Command not in whitelist: ${command}`)
    }

    try {
      const result = await execa(command, {
        shell: true,
        timeout,
        cwd: process.cwd(),
        env: process.env
      })

      return {
        stdout: result.stdout,
        stderr: result.stderr
      }
    } catch (error: any) {
      throw new Error(`Command failed: ${command} - ${error.message}`)
    }
  }

  private isCommandAllowed(command: string): boolean {
    return this.config.whitelistCommands.some(allowed => {
      // Exact match or command starts with allowed pattern
      return command === allowed || command.startsWith(allowed + ' ')
    })
  }

  async runSafeCommand(command: string, description: string): Promise<{ success: boolean; output: string; error?: string }> {
    try {
      const result = await this.runCommand(command)
      return {
        success: true,
        output: result.stdout
      }
    } catch (error: any) {
      return {
        success: false,
        output: '',
        error: error.message
      }
    }
  }
}
