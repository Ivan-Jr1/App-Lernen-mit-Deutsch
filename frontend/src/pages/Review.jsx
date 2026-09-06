import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { api } from '../api.js'
import { EmptyState, ErrorBox, Loading } from '../components/States.jsx'
import { useUser } from '../user.jsx'

// Notas do SM-2: < 3 reinicia o intervalo, >= 3 avança.
const GRADES = [
  { value: 0, label: 'Em branco', tone: 'bad' },
  { value: 1, label: 'Muito difícil', tone: 'bad' },
  { value: 2, label: 'Difícil', tone: 'bad' },
  { value: 3, label: 'Ok', tone: 'ok' },
  { value: 4, label: 'Fácil', tone: 'good' },
  { value: 5, label: 'Fácil demais', tone: 'good' },
]

const TONE_CLASSES = {
  bad: 'border-red-200 bg-red-50 text-red-700 hover:bg-red-100',
  ok: 'border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100',
  good: 'border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100',
}

function nextIntervalLabel(days) {
  if (days <= 1) return 'amanhã'
  if (days < 30) return `em ${days} dias`
  return `em ${Math.round(days / 30)} meses`
}

export default function Review() {
  const { username } = useUser()
  const [queue, setQueue] = useState(null)
  const [error, setError] = useState(null)
  const [revealed, setRevealed] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [reviewedCount, setReviewedCount] = useState(0)
  const [lastResult, setLastResult] = useState(null)

  const load = useCallback(() => {
    setQueue(null)
    setError(null)
    setRevealed(false)
    setReviewedCount(0)
    setLastResult(null)
    api
      .dueCards(username)
      .then(setQueue)
      .catch((err) => setError(err.message))
  }, [username])

  useEffect(load, [load])

  async function grade(value) {
    const card = queue[0]
    setSubmitting(true)
    try {
      const result = await api.submitReview(username, card.id, value)
      setLastResult({ grade: value, ...result })
      setReviewedCount((count) => count + 1)
      setQueue((current) => current.slice(1))
      setRevealed(false)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (error) return <ErrorBox message={error} onRetry={load} />
  if (queue === null) return <Loading label="Buscando cartões vencidos…" />

  if (queue.length === 0) {
    return (
      <EmptyState>
        <p className="text-lg font-semibold text-slate-700">Tudo revisado! 🎉</p>
        <p className="mt-1 text-sm">
          {reviewedCount > 0
            ? `${reviewedCount} ${reviewedCount === 1 ? 'cartão revisado' : 'cartões revisados'} nesta sessão.`
            : 'Nenhum cartão vencido agora. Volte mais tarde.'}
        </p>
        <Link
          to="/dashboard"
          className="mt-4 inline-block text-sm font-medium text-slate-900 underline underline-offset-2"
        >
          Ver o dashboard
        </Link>
      </EmptyState>
    )
  }

  const card = queue[0]

  return (
    <div>
      <div className="mb-4 flex items-center justify-between text-sm text-slate-500">
        <span>{queue.length} na fila</span>
        <span>{reviewedCount} revisados</span>
      </div>

      {lastResult && (
        <p className="mb-4 rounded-lg bg-slate-100 px-3 py-2 text-sm text-slate-600">
          +{lastResult.points_earned} pts · próxima revisão {nextIntervalLabel(lastResult.new_interval)}
        </p>
      )}

      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">
        {card.category && (
          <span className="text-xs font-medium uppercase tracking-wide text-slate-400">
            {card.category}
          </span>
        )}
        <p className="mt-2 text-2xl font-semibold text-slate-900">{card.front_pt}</p>

        {revealed ? (
          <div className="mt-6 border-t border-slate-100 pt-6">
            <p className="text-2xl font-bold text-slate-900">{card.back_de}</p>
            {card.phonetic_hint && (
              <p className="mt-1 text-sm italic text-slate-500">🔊 {card.phonetic_hint}</p>
            )}
          </div>
        ) : (
          <button
            onClick={() => setRevealed(true)}
            className="mt-6 rounded-lg bg-slate-900 px-5 py-2 text-sm font-medium text-white hover:bg-slate-700"
          >
            Mostrar resposta
          </button>
        )}
      </div>

      {revealed && (
        <div className="mt-6">
          <p className="mb-2 text-center text-sm text-slate-500">Quão bem você lembrou?</p>
          <div className="grid grid-cols-3 gap-2 sm:grid-cols-6">
            {GRADES.map((option) => (
              <button
                key={option.value}
                disabled={submitting}
                onClick={() => grade(option.value)}
                className={`flex flex-col items-center rounded-lg border px-2 py-3 text-xs font-medium transition disabled:opacity-50 ${TONE_CLASSES[option.tone]}`}
              >
                <span className="text-base font-bold">{option.value}</span>
                {option.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
