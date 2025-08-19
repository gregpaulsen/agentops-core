'use client'

import { useState, useEffect } from 'react'

interface DoctorStatus {
  lastRun: string | null
  summary: {
    ok: number
    warn: number
    fail: number
  }
  failingChecks: string[]
  mode: string
  timestamp: string
}

interface AuditLog {
  id: string
  action: string
  entity: string
  timestamp: string
  metadata: any
}

interface TelemetryEvent {
  id: string
  type: string
  timestamp: string
  payload: any
}

export default function AdminPage() {
  const [doctorStatus, setDoctorStatus] = useState<DoctorStatus | null>(null)
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([])
  const [telemetryEvents, setTelemetryEvents] = useState<TelemetryEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [runningDoctor, setRunningDoctor] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [statusRes, auditRes, telemetryRes] = await Promise.all([
        fetch('/api/doctor/status'),
        fetch('/api/audit/latest'),
        fetch('/api/telemetry/latest')
      ])

      if (statusRes.ok) {
        const status = await statusRes.json()
        setDoctorStatus(status)
      }

      if (auditRes.ok) {
        const audit = await auditRes.json()
        setAuditLogs(audit.logs || [])
      }

      if (telemetryRes.ok) {
        const telemetry = await telemetryRes.json()
        setTelemetryEvents(telemetry.events || [])
      }
    } catch (error) {
      console.error('Failed to load admin data:', error)
    } finally {
      setLoading(false)
    }
  }

  const runDoctor = async (mode: 'scan' | 'repair') => {
    setRunningDoctor(true)
    try {
      const response = await fetch('/api/doctor/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token'
        },
        body: JSON.stringify({ mode })
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Doctor run completed:', result)
        // Reload data to show updated status
        await loadData()
      } else {
        console.error('Doctor run failed:', await response.text())
      }
    } catch (error) {
      console.error('Failed to run doctor:', error)
    } finally {
      setRunningDoctor(false)
    }
  }

  const getStatusColor = (status: DoctorStatus) => {
    if (status.summary.fail > 0) return 'text-red-600'
    if (status.summary.warn > 0) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getStatusText = (status: DoctorStatus) => {
    if (status.summary.fail > 0) return 'FAIL'
    if (status.summary.warn > 0) return 'WARN'
    return 'PASS'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Loading Admin Panel...</h1>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">PaulyOps Admin Panel</h1>

        {/* System Doctor Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">System Doctor</h2>
            <div className="flex space-x-2">
              <button
                onClick={() => runDoctor('scan')}
                disabled={runningDoctor}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {runningDoctor ? 'Running...' : 'Scan'}
              </button>
              <button
                onClick={() => runDoctor('repair')}
                disabled={runningDoctor}
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
              >
                {runningDoctor ? 'Running...' : 'Repair'}
              </button>
            </div>
          </div>

          {doctorStatus && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className={`text-2xl font-bold ${getStatusColor(doctorStatus)}`}>
                  {getStatusText(doctorStatus)}
                </div>
                <div className="text-sm text-gray-600">Status</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{doctorStatus.summary.ok}</div>
                <div className="text-sm text-gray-600">OK</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">{doctorStatus.summary.warn}</div>
                <div className="text-sm text-gray-600">Warnings</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">{doctorStatus.summary.fail}</div>
                <div className="text-sm text-gray-600">Failures</div>
              </div>
            </div>
          )}

          {doctorStatus?.failingChecks && doctorStatus.failingChecks.length > 0 && (
            <div className="mt-4">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Failing Checks:</h3>
              <ul className="list-disc list-inside text-red-600">
                {doctorStatus.failingChecks.map((check, index) => (
                  <li key={index}>{check}</li>
                ))}
              </ul>
            </div>
          )}

          {doctorStatus?.lastRun && (
            <div className="mt-4 text-sm text-gray-600">
              Last run: {new Date(doctorStatus.lastRun).toLocaleString()}
            </div>
          )}
        </div>

        {/* Audit Logs */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Latest Audit Logs</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Action
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Entity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {auditLogs.map((log) => (
                  <tr key={log.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {log.action}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.entity}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Telemetry Events */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Latest Telemetry Events</h2>
          <div className="space-y-2">
            {telemetryEvents.map((event) => (
              <div key={event.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <div className="font-medium text-gray-900">{event.type}</div>
                  <div className="text-sm text-gray-500">
                    {new Date(event.timestamp).toLocaleString()}
                  </div>
                </div>
                <div className="text-sm text-gray-500">
                  {JSON.stringify(event.payload).substring(0, 50)}...
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
