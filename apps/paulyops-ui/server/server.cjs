const express = require('express');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

// ===== Config (edit if needed) =====
const HOME = process.env.HOME || process.env.USERPROFILE || '';
const REPORT_MD = process.env.HEALTH_REPORT_PATH || path.join(HOME, 'Desktop', 'System_Health_Report.md');
const REPORTS_DIR = process.env.REPORTS_DIR || path.join(HOME, 'Desktop', 'Reports');
const ALLOW_ACTIONS = (process.env.ALLOW_ACTIONS || 'true').toLowerCase() === 'true';
const HEALTH_CMD = path.join(HOME, 'Desktop', 'Coding_Commands', 'system_health.command');
const NIGHTLY_CMD = path.join(HOME, 'Desktop', 'Coding_Commands', 'nightly_report.command');
// ==================================

// Safe file reading function
function safeReadFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf-8');
    }
    return null;
  } catch (e) {
    console.log(`Warning: Could not read ${filePath}: ${e.message}`);
    return null;
  }
}

// Parse the markdown table from System_Health_Report.md into JSON rows
function parseHealthTable(md) {
  if (!md) return [];
  const lines = md.split(/\r?\n/);
  const start = lines.findIndex(l => l.trim().startsWith('| Check ') && l.includes('| Status '));
  if (start === -1) return [];
  const dataLines = lines.slice(start + 2).filter(l => l.trim().startsWith('|'));
  return dataLines.map(line => {
    const cells = line.split('|').slice(1, -1).map(c => c.trim());
    return { check: cells[0], status: cells[1], details: cells[2] };
  });
}

// GET /api/health/report → parsed health table + overall flag
app.get('/api/health/report', (req, res) => {
  try {
    const md = safeReadFile(REPORT_MD);
    if (!md) {
      return res.json({ 
        overall: false, 
        rows: [
          { check: 'System Health Report', status: '❌ FAIL', details: 'Report file not found - run system health first' }
        ],
        error: 'Report not found - run system health command first'
      });
    }
    const rows = parseHealthTable(md);
    const overall = md.includes('**Overall:** ✅ PASS');
    res.json({ overall, rows });
  } catch (e) {
    res.json({ 
      overall: false, 
      rows: [{ check: 'System Health Report', status: '❌ ERROR', details: e.message }],
      error: e.message 
    });
  }
});

// GET /api/reports/nightly/latest → read most recent Nightly_Update_Report_YYYY-MM-DD.md
app.get('/api/reports/nightly/latest', (req, res) => {
  try {
    if (!fs.existsSync(REPORTS_DIR)) {
      return res.json({ content: 'No reports directory found. Run nightly report first.' });
    }
    
    const files = fs.readdirSync(REPORTS_DIR)
      .filter(f => f.startsWith('Nightly_Update_Report_') && f.endsWith('.md'))
      .map(f => ({ f, m: fs.statSync(path.join(REPORTS_DIR, f)).mtimeMs }))
      .sort((a, b) => b.m - a.m);
    
    if (!files.length) {
      return res.json({ content: 'No nightly reports found. Run nightly report first.' });
    }
    
    const latestPath = path.join(REPORTS_DIR, files[0].f);
    const content = safeReadFile(latestPath);
    res.json({ path: latestPath, content: content || 'Could not read report file' });
  } catch (e) {
    res.json({ content: `Error reading reports: ${e.message}` });
  }
});

// POST /api/actions/run-health → runs system health command
app.post('/api/actions/run-health', (req, res) => {
  if (!ALLOW_ACTIONS) return res.status(403).json({ error: 'Actions disabled' });
  
  // Check if command exists
  if (!fs.existsSync(HEALTH_CMD)) {
    return res.status(404).json({ 
      error: 'Health command not found', 
      path: HEALTH_CMD,
      message: 'Please ensure system_health.command exists in ~/Desktop/Coding_Commands/' 
    });
  }
  
  exec(`"${HEALTH_CMD}"`, { timeout: 5 * 60_000 }, (err, stdout, stderr) => {
    if (err) return res.status(500).json({ error: err.message, stdout, stderr });
    res.json({ ok: true, stdout: stdout.slice(-4000) });
  });
});

// POST /api/actions/send-nightly → runs nightly report command
app.post('/api/actions/send-nightly', (req, res) => {
  if (!ALLOW_ACTIONS) return res.status(403).json({ error: 'Actions disabled' });
  
  // Check if command exists
  if (!fs.existsSync(NIGHTLY_CMD)) {
    return res.status(404).json({ 
      error: 'Nightly command not found', 
      path: NIGHTLY_CMD,
      message: 'Please ensure nightly_report.command exists in ~/Desktop/Coding_Commands/' 
    });
  }
  
  exec(`"${NIGHTLY_CMD}"`, { timeout: 5 * 60_000 }, (err, stdout, stderr) => {
    if (err) return res.status(500).json({ error: err.message, stdout, stderr });
    res.json({ ok: true, stdout: stdout.slice(-4000) });
  });
});

// Demo tenant endpoints (placeholder)
app.get('/api/branding', (_req, res) => {
  res.json({ name: 'Big Sky Ag', logo: null, primaryColor: '#0ea5e9' });
});

app.get('/api/features', (_req, res) => {
  res.json({ backupRotation: true, nightlyEmail: true, actionsEnabled: ALLOW_ACTIONS });
});

// Health check endpoint
app.get('/api/health', (_req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    config: {
      reportPath: REPORT_MD,
      reportsDir: REPORTS_DIR,
      healthCmd: HEALTH_CMD,
      nightlyCmd: NIGHTLY_CMD,
      allowActions: ALLOW_ACTIONS
    }
  });
});

const PORT = Number(process.env.PORT || 8787);

// Add error handling to prevent hanging
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

app.listen(PORT, () => {
  console.log(`🚀 Bridge listening on http://localhost:${PORT}`);
  console.log(`📁 Report path: ${REPORT_MD}`);
  console.log(`📁 Reports dir: ${REPORTS_DIR}`);
  console.log(`⚡ Actions enabled: ${ALLOW_ACTIONS}`);
});
