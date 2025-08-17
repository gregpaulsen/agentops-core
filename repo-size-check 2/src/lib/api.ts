export async function getHealth() {
  const r = await fetch('/api/health/report')
  if (!r.ok) throw new Error('health fetch failed')
  return r.json() as Promise<{ overall: boolean; rows: any[] }>
}
export async function getNightlyLatest() {
  const r = await fetch('/api/reports/nightly/latest')
  if (!r.ok) throw new Error('nightly fetch failed')
  return r.json() as Promise<{ path: string; content: string }>
}
export async function runHealth() {
  const r = await fetch('/api/actions/run-health', { method: 'POST' })
  if (!r.ok) throw new Error('run health failed')
  return r.json()
}
export async function sendNightly() {
  const r = await fetch('/api/actions/send-nightly', { method: 'POST' })
  if (!r.ok) throw new Error('send nightly failed')
  return r.json()
}
