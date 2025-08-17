import express from 'express'
import fs from 'fs'
import path from 'path'
import { exec } from 'child_process'

const app = express()
app.use(express.json())

// ===== Config (edit if needed) =====
const HOME = process.env.HOME || process.env.USERPROFILE || ''
const REPORT_MD = process.env.HEALTH_REPORT_PATH || path.join(HOME, 'Desktop', 'System_Health_Report.md')
const REPORTS_DIR = process.env.REPORTS_DIR || path.join(HOME, 'Desktop', 'Reports')
const ALLOW_ACTIONS = (process.env.ALLOW_ACTIONS || 'true').toLowerCase() === 'true'
const HEALTH_CMD = path.join(HOME, 'Desktop', 'Coding_Commands', 'system_health.command')
const NIGHTLY_CMD = path.join(HOME, 'Desktop', 'Coding_Commands', 'nightly_report.command')
// ==================================

// Parse the markdown table from System_Health_Report.md into JSON rows
function parseHealthTable(md: string) {
  const lines = md.split(/\r?\n/)
  const start = lines.findIndex(l => l.trim().startsWith('| Check ') && l.includes('| Status '))
  if (start === -1) return []
  const dataLines = lines.slice(start + 2).filter(l => l.trim().startsWith('|'))
  return dataLines.map(line => {
    const cells = line.split('|').slice(1, -1).map(c => c.trim())
    return { check: cells[0], status: cells[1], details: cells[2] }
  })
}

// GET /api/health/report → parsed health table + overall flag
app.get('/api/health/report', (req, res) => {
  try {
    const md = fs.readFileSync(REPORT_MD, 'utf-8')
    const rows = parseHealthTable(md)
    const overall = md.includes('**Overall:** ✅ PASS')
    res.json({ overall, rows })
  } catch (e: any) {
    res.status(404).json({ error: 'Report not found', path: REPORT_MD, message: e?.message })
  }
})

// GET /api/reports/nightly/latest → read most recent Nightly_Update_Report_YYYY-MM-DD.md
app.get('/api/reports/nightly/latest', (req, res) => {
  try {
    const files = fs.readdirSync(REPORTS_DIR)
      .filter(f => f.startsWith('Nightly_Update_Report_') && f.endsWith('.md'))
      .map(f => ({ f, m: fs.statSync(path.join(REPORTS_DIR, f)).mtimeMs }))
      .sort((a, b) => b.m - a.m)
    if (!files.length) return res.status(404).json({ error: 'No nightly reports found' })
    const latestPath = path.join(REPORTS_DIR, files[0].f)
    const content = fs.readFileSync(latestPath, 'utf-8')
    res.json({ path: latestPath, content })
  } catch (e: any) {
    res.status(404).json({ error: 'Nightly report dir not found', path: REPORTS_DIR, message: e?.message })
  }
})

// POST /api/actions/run-health → runs system health command
app.post('/api/actions/run-health', (req, res) => {
  if (!ALLOW_ACTIONS) return res.status(403).json({ error: 'Actions disabled' })
  exec(`"${HEALTH_CMD}"`, { timeout: 5 * 60_000 }, (err, stdout, stderr) => {
    if (err) return res.status(500).json({ error: err.message, stdout, stderr })
    res.json({ ok: true, stdout: stdout.slice(-4000) })
  })
})

// POST /api/actions/send-nightly → runs nightly report command
app.post('/api/actions/send-nightly', (req, res) => {
  if (!ALLOW_ACTIONS) return res.status(403).json({ error: 'Actions disabled' })
  exec(`"${NIGHTLY_CMD}"`, { timeout: 5 * 60_000 }, (err, stdout, stderr) => {
    if (err) return res.status(500).json({ error: err.message, stdout, stderr })
    res.json({ ok: true, stdout: stdout.slice(-4000) })
  })
})

// Demo tenant endpoints (placeholder)
app.get('/api/branding', (_req, res) => {
  res.json({ name: 'Big Sky Ag', logo: null, primaryColor: '#0ea5e9' })
})
app.get('/api/features', (_req, res) => {
  res.json({ backupRotation: true, nightlyEmail: true, actionsEnabled: ALLOW_ACTIONS })
})

const PORT = Number(process.env.PORT || 8787)
app.listen(PORT, () => console.log(`Bridge listening on http://localhost:${PORT}`))
