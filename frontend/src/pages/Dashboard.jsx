import { useCallback, useEffect, useState } from 'react'

import { api } from '../lib/api.js'
import { Card, ErrorState, Spinner } from '../components/ui.jsx'
import { FlameIcon } from '../components/icons.jsx'

const days = (value) => `${value} ${value === 1 ? 'dia' : 'dias'}`

const METRICS = [
  { key: 'total_points', label: 'Pontos' },
  { key: 'current_streak', label: 'Streak atual', format: days },
  { key: 'longest_streak', label: 'Streak recorde', format: days },
  { key: 'reviewed_today', label: 'Cartões hoje' },
  { key: 'total_cards_reviewed', label: 'Cartões revisados' },
  { key: 'scenarios_completed', label: 'Cenários completados' },
]

function HeroCard({ user, leads }) {
  return (
    <Card className="p-5 text-center">
      <p className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
        {leads && <span className="mr-1">👑</span>}
        {user.display_name}
      </p>
      <p className="mt-1 text-4xl font-extrabold tracking-tight tabular-nums">
        {user.total_points}
      </p>
      <p className="text-xs text-zinc-400">pontos</p>
      <div className="mt-3 inline-flex items-center gap-1.5 rounded-full bg-amber-100 px-2.5 py-1 text-sm font-semibold text-amber-700 dark:bg-amber-950/50 dark:text-amber-300">
        <FlameIcon className="size-4" />
        {days(user.current_streak)}
      </div>

      <div className="mt-3">
        <p className="text-xs font-medium tabular-nums text-zinc-500 dark:text-zinc-400">
          Meta de hoje: {user.reviewed_today}/{user.daily_goal}
        </p>
        <div className="mx-auto mt-1 h-1.5 w-24 overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800">
          <div
            className="h-full rounded-full bg-accent-500 transition-[width] duration-500"
            style={{ width: `${Math.min(100, (user.reviewed_today / user.daily_goal) * 100)}%` }}
          />
        </div>
      </div>

      {user.cards_due_today > 0 && (
        <p className="mt-3 text-xs text-zinc-500 dark:text-zinc-400">
          {user.cards_due_today} cartões esperando hoje
        </p>
      )}
    </Card>
  )
}

function ComparisonRow({ label, a, b, format }) {
  const fmt = format ?? String
  const total = a + b
  const aShare = total === 0 ? 50 : (a / total) * 100
  const leader = a === b ? null : a > b ? 'a' : 'b'

  return (
    <div className="py-3">
      <div className="mb-1.5 flex items-center justify-between text-sm">
        <span className={`tabular-nums ${leader === 'a' ? 'font-bold' : 'text-zinc-500 dark:text-zinc-400'}`}>
          {fmt(a)}
        </span>
        <span className="text-xs font-medium uppercase tracking-wide text-zinc-400">{label}</span>
        <span className={`tabular-nums ${leader === 'b' ? 'font-bold' : 'text-zinc-500 dark:text-zinc-400'}`}>
          {fmt(b)}
        </span>
      </div>
      <div className="flex h-2 overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800">
        <div className="bg-accent-500 transition-[width] duration-500" style={{ width: `${aShare}%` }} />
        <div className="flex-1 bg-emerald-500" />
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const load = useCallback(() => {
    setError(null)
    api.dashboard().then(setData).catch((err) => setError(err.message))
  }, [])

  useEffect(load, [load])

  if (error) return <ErrorState message={error} onRetry={load} />
  if (data === null) return <Spinner />

  const [a, b] = data.users

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3">
        <HeroCard user={a} leads={a.total_points > b.total_points} />
        <HeroCard user={b} leads={b.total_points > a.total_points} />
      </div>

      <Card className="px-5 py-2">
        <div className="flex justify-between py-2 text-xs font-semibold uppercase tracking-wide">
          <span className="text-accent-600 dark:text-accent-400">{a.display_name}</span>
          <span className="text-emerald-600 dark:text-emerald-400">{b.display_name}</span>
        </div>
        <div className="divide-y divide-zinc-100 dark:divide-zinc-800">
          {METRICS.map((metric) => (
            <ComparisonRow
              key={metric.key}
              label={metric.label}
              a={a[metric.key]}
              b={b[metric.key]}
              format={metric.format}
            />
          ))}
        </div>
      </Card>

      <p className="text-center text-xs text-zinc-400">
        Competição amigável — o objetivo é os dois chegarem em Berlim falando alemão.
      </p>
    </div>
  )
}
