#!/usr/bin/env node

import { runDoctor } from '../index'
import { DoctorMode } from '../types'

async function main() {
  const args = process.argv.slice(2)
  const mode = args[0] as DoctorMode

  if (!mode || !['scan', 'repair', 'surgical'].includes(mode)) {
    console.error('Usage: doctor <scan|repair|surgical>')
    console.error('')
    console.error('Modes:')
    console.error('  scan     - Run health checks only (read-only)')
    console.error('  repair   - Run checks and attempt safe repairs')
    console.error('  surgical - Run checks and attempt all repairs (including rollbacks)')
    process.exit(1)
  }

  try {
    console.log(`🩺 PaulyOps System Doctor - ${mode.toUpperCase()} mode`)
    console.log('=' .repeat(50))
    
    const startTime = Date.now()
    const report = await runDoctor({ mode })
    const duration = Date.now() - startTime

    // Print summary table
    console.log('\n📊 Health Check Summary')
    console.log('-' .repeat(50))
    console.log(`✅ OK:     ${report.summary.ok}`)
    console.log(`⚠️  WARN:   ${report.summary.warn}`)
    console.log(`❌ FAIL:   ${report.summary.fail}`)
    console.log(`⏱️  Time:   ${duration}ms`)

    if (report.failingChecks.length > 0) {
      console.log('\n❌ Failing Checks:')
      report.failingChecks.forEach(check => {
        console.log(`   • ${check}`)
      })
    }

    if (report.repairs.length > 0) {
      console.log('\n🔧 Repairs Attempted:')
      report.repairs.forEach(repair => {
        const status = repair.success ? '✅' : '❌'
        console.log(`   ${status} ${repair.check}: ${repair.action.description}`)
      })
    }

    if (report.savepoint) {
      console.log(`\n💾 Savepoint: ${report.savepoint}`)
    }

    console.log('\n📄 Detailed Results:')
    console.log('-' .repeat(50))
    report.checks.forEach(check => {
      const status = check.status === 'ok' ? '✅' : check.status === 'warn' ? '⚠️' : '❌'
      const duration = check.duration ? ` (${check.duration}ms)` : ''
      console.log(`${status} ${check.name}: ${check.message}${duration}`)
    })

    console.log('\n' + '=' .repeat(50))
    
    if (report.summary.fail > 0) {
      console.log('❌ System has issues that require attention')
      process.exit(1)
    } else {
      console.log('✅ System is healthy!')
      process.exit(0)
    }
  } catch (error: any) {
    console.error('💥 Doctor failed:', error.message)
    process.exit(1)
  }
}

if (require.main === module) {
  main()
}
