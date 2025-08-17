export type HealthRow = { check: string; status: string; details: string }

export default function HealthTable({ rows }: { rows: HealthRow[] }) {
  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-black/5">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Check</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Status</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600">Details</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {rows.map((r, i) => (
            <tr key={i} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm text-gray-900">{r.check}</td>
              <td className="px-4 py-3 text-sm">
                <span className={`inline-flex items-center gap-2 rounded-full px-2.5 py-1 text-xs font-medium ${r.status.includes('PASS') ? 'bg-green-50 text-green-700 ring-1 ring-green-600/20' : 'bg-red-50 text-red-700 ring-1 ring-red-600/20'}`}>
                  {r.status}
                </span>
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">{r.details}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
