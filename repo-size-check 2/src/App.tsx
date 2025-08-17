import { useEffect, useState } from 'react'
import StatCard from './components/StatCard'
import HealthTable, { HealthRow } from './components/HealthTable'
import { getHealth, getNightlyLatest, runHealth, sendNightly } from './lib/api'
import { CheckCircle, AlertTriangle, Mail, RefreshCw, Server, Clock, Play } from 'lucide-react'

export default function App() {
  const [loading, setLoading] = useState(true)
  const [overall, setOverall] = useState<boolean | null>(null)
  const [rows, setRows] = useState<HealthRow[]>([])
  const [nightly, setNightly] = useState<string>('')
  const [busy, setBusy] = useState<'run' | 'send' | null>(null)
  const ok = (s: string) => s.includes('PASS') || s.includes('✅')

  async function load() {
    setLoading(true)
    try {
      const h = await getHealth()
      setOverall(h.overall)
      setRows(h.rows)
      try {
        const n = await getNightlyLatest()
        setNightly(n.content)
      } catch { /* nightly optional */ }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const stat = (check: string) => rows.find(r => r.check === check)

  return (
    <div className="min-h-screen p-6 md:p-10">
      <header className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Big Sky / PaulyOps — Ops Dashboard</h1>
          <p className="text-sm text-gray-600">Local automation health & controls</p>
        </div>
        <div className="flex gap-2">
          <button onClick={async () => { setBusy('run'); await runHealth().catch(()=>{}); setBusy(null); load() }} className="inline-flex items-center gap-2 rounded-xl bg-gray-900 text-white px-4 py-2 disabled:opacity-50">
            <RefreshCw className="w-4 h-4" /> {busy==='run' ? 'Running…' : 'Run Health'}
          </button>
          <button onClick={async () => { setBusy('send'); await sendNightly().catch(()=>{}); setBusy(null); load() }} className="inline-flex items-center gap-2 rounded-xl bg-brand text-white px-4 py-2 disabled:opacity-50">
            <Mail className="w-4 h-4" /> {busy==='send' ? 'Sending…' : 'Send Nightly Now'}
          </button>
        </div>
      </header>

      {loading ? (
        <div className="text-gray-600">Loading health…</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-6">
            <StatCard title="Overall" value={overall ? <span className="inline-flex items-center gap-2 text-green-700"><CheckCircle className="w-5 h-5"/>PASS</span> : <span className="inline-flex items-center gap-2 text-red-700"><AlertTriangle className="w-5 h-5"/>ATTN</span>} hint="Aggregated from System_Health_Report.md" />
            <StatCard title="Backups" value={ok(stat('Backup freshness')?.status || '') ? 'Fresh' : 'Stale'} hint={stat('Backup freshness')?.details} icon={<Server className="w-5 h-5 text-gray-500"/>} />
            <StatCard title="Rotation" value={ok(stat('Backup rotation')?.status || '') ? 'OK' : 'Check'} hint={stat('Backup rotation')?.details} />
            <StatCard title="Router" value={ok(stat('Router logs recent')?.status || '') ? 'OK' : 'No activity'} hint={stat('Router logs recent')?.details} />
            <StatCard title="launchd" value={ok(stat('launchd jobs')?.status || '') ? 'Loaded' : 'Missing'} hint={stat('launchd jobs')?.details} />
            <StatCard title="Nightly Email" value={ok(stat('Nightly Email Sent')?.status || '') ? 'Sent <26h' : 'Not sent'} hint={stat('Nightly Email Sent')?.details} icon={<Clock className="w-5 h-5 text-gray-500"/>} />
          </div>

          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">Health Checks</h2>
            <HealthTable rows={rows} />
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-2">Latest Nightly Report</h2>
            <div className="rounded-2xl bg-white shadow-sm ring-1 ring-black/5 p-4 whitespace-pre-wrap text-sm text-gray-800 max-h-[420px] overflow-auto">
              {nightly || 'No nightly report found.'}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
