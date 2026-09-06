import { useCallback, useEffect, useState } from 'react'

import { api } from '../api.js'
import { ErrorBox, Loading } from '../components/States.jsx'

const days = (value) => `${value} ${value === 1 ? 'dia' : 'dias'}`

const METRICS = [
  { key: 'total_points', label: 'Pontos' },
  { key: 'current_streak', label: 'Streak atual', format: days },
  { key: 'longest_streak', label: 'Streak recorde', format: days },
  { key: 'total_cards_reviewed', label: 'Cartões revisados' },
  { key: 'scenarios_completed', label: 'Cenários completados' },
  // informativo, não é disputa: mais cartões vencidos significa estar atrasado
  { key: 'cards_due_today', label: 'Cartões para hoje', neutral: true },
]

function leaderIndex(users, metric) {
  if (metric.neutral) return -1
  const [a, b] = users.map((user) => user[metric.key])
  if (a === b) return -1
  return a > b ? 0 : 1
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const load = useCallback(() => {
    setError(null)
    api.dashboard().then(setData).catch((err) => setError(err.message))
  }, [])

  useEffect(load, [load])

  if (error) return <ErrorBox message={error} onRetry={load} />
  if (data === null) return <Loading />

  const users = data.users

  return (
    <div>
      <div className="mb-6 grid grid-cols-2 gap-3">
        {users.map((user) => (
          <div
            key={user.username}
            className="rounded-2xl border border-slate-200 bg-white p-5 text-center shadow-sm"
          >
            <p className="text-sm font-medium text-slate-500">{user.display_name}</p>
            <p className="mt-1 text-3xl font-bold text-slate-900">{user.total_points}</p>
            <p className="text-xs text-slate-400">pontos</p>
            <p className="mt-2 text-sm">
              🔥 {user.current_streak} {user.current_streak === 1 ? 'dia' : 'dias'}
            </p>
          </div>
        ))}
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
              <th className="px-4 py-3 text-left font-medium">Métrica</th>
              {users.map((user) => (
                <th key={user.username} className="px-4 py-3 text-right font-medium">
                  {user.display_name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {METRICS.map((metric) => {
              const leader = leaderIndex(users, metric)
              return (
                <tr key={metric.key} className="border-b border-slate-50 last:border-0">
                  <td className="px-4 py-3 text-slate-600">{metric.label}</td>
                  {users.map((user, index) => (
                    <td
                      key={user.username}
                      className={`px-4 py-3 text-right tabular-nums ${
                        leader === index ? 'font-bold text-slate-900' : 'text-slate-500'
                      }`}
                    >
                      {metric.format ? metric.format(user[metric.key]) : user[metric.key]}
                      {leader === index && ' ↑'}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <p className="mt-4 text-center text-xs text-slate-400">
        Competição amigável — o objetivo é os dois chegarem em Berlim falando alemão.
      </p>
    </div>
  )
}
