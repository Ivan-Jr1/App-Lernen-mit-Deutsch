import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext.jsx'
import { api } from '../lib/api.js'
import {
  getSpeechRate,
  setSpeechRate,
  speak,
  SPEECH_SPEED_PRESETS,
  speechSupported,
  stopSpeaking,
} from '../lib/speech.js'
import { languageName } from '../lib/languages.js'
import { SpeakerIcon, SpeakerOffIcon } from '../components/icons.jsx'
import { Button, EmptyState, ErrorState, Spinner } from '../components/ui.jsx'

// Notas do SM-2: < 3 reinicia o intervalo, >= 3 avança.
const GRADES = [
  { value: 0, label: 'Em branco', tone: 'bad' },
  { value: 1, label: 'Muito difícil', tone: 'bad' },
  { value: 2, label: 'Difícil', tone: 'bad' },
  { value: 3, label: 'Ok', tone: 'ok' },
  { value: 4, label: 'Fácil', tone: 'good' },
  { value: 5, label: 'Fácil demais', tone: 'good' },
]

const TONE = {
  bad: 'border-rose-200 text-rose-700 hover:bg-rose-50 dark:border-rose-900/60 dark:text-rose-300 dark:hover:bg-rose-950/40',
  ok: 'border-amber-200 text-amber-700 hover:bg-amber-50 dark:border-amber-900/60 dark:text-amber-300 dark:hover:bg-amber-950/40',
  good: 'border-emerald-200 text-emerald-700 hover:bg-emerald-50 dark:border-emerald-900/60 dark:text-emerald-300 dark:hover:bg-emerald-950/40',
}

const MUTE_KEY = 'deutsch-app:mute-speech'

function nextIntervalLabel(days) {
  if (days <= 1) return 'amanhã'
  if (days < 30) return `em ${days} dias`
  if (days < 365) return `em ${Math.round(days / 30)} meses`
  return `em ${(days / 365).toFixed(1)} anos`
}

function Flashcard({ card, flipped, onFlip, onSpeak }) {
  return (
    <div className="[perspective:1400px]">
      <button
        onClick={onFlip}
        className="relative block h-72 w-full text-left [transition:transform_0.5s] preserve-3d"
        style={{ transform: flipped ? 'rotateY(180deg)' : 'none' }}
        aria-label={flipped ? 'Ver a frente' : 'Ver a resposta'}
      >
        {/* Frente — português */}
        <span className="backface-hidden absolute inset-0 flex flex-col items-center justify-center rounded-3xl border border-zinc-200 bg-white p-8 text-center shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          {card.category && (
            <span className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
              {card.category}
            </span>
          )}
          <span className="mt-3 text-3xl font-bold text-zinc-900 dark:text-zinc-50">
            {card.front_pt}
          </span>
          <span className="mt-6 text-xs text-zinc-400">toque para ver a resposta</span>
        </span>

        {/* Verso — idioma estudado */}
        <span className="backface-hidden rotate-y-180 absolute inset-0 flex flex-col items-center justify-center rounded-3xl border border-accent-200 bg-accent-50 p-8 text-center shadow-sm dark:border-accent-900/60 dark:bg-accent-950/40">
          <span className="text-sm text-accent-700/60 dark:text-accent-300/60">{card.front_pt}</span>
          <span className="mt-2 flex items-center gap-2 text-3xl font-bold text-accent-950 dark:text-accent-100">
            {card.back_target}
            {speechSupported && (
              <span
                role="button"
                tabIndex={-1}
                onClick={(e) => {
                  e.stopPropagation()
                  onSpeak()
                }}
                aria-label={`Ouvir em ${languageName(card.language)}`}
                className="grid size-8 place-items-center rounded-full bg-accent-600 text-white hover:bg-accent-500"
              >
                <SpeakerIcon className="size-4" />
              </span>
            )}
          </span>
          {card.phonetic_hint && (
            <span className="mt-2 text-sm italic text-accent-700/80 dark:text-accent-300/80">
              {card.phonetic_hint}
            </span>
          )}
        </span>
      </button>
    </div>
  )
}

export default function Review() {
  const { isGuest } = useAuth()
  const [queue, setQueue] = useState(null)
  const [error, setError] = useState(null)
  const [flipped, setFlipped] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [done, setDone] = useState(0)
  const [goal, setGoal] = useState(0)
  const [reviewedToday, setReviewedToday] = useState(0)
  const [dueTotal, setDueTotal] = useState(0)
  const [lastResult, setLastResult] = useState(null)
  const [muted, setMuted] = useState(() => {
    try {
      return localStorage.getItem(MUTE_KEY) === '1'
    } catch {
      return false
    }
  })
  const [speechRate, setSpeechRateState] = useState(getSpeechRate)

  // Percorre as velocidades disponíveis (da mais lenta à mais rápida, com volta).
  function cycleSpeechRate() {
    const index = SPEECH_SPEED_PRESETS.findIndex((preset) => preset.value === speechRate)
    const next = SPEECH_SPEED_PRESETS[(index + 1) % SPEECH_SPEED_PRESETS.length]
    setSpeechRate(next.value)
    setSpeechRateState(next.value)
  }

  const load = useCallback((includeAll = false) => {
    setQueue(null)
    setError(null)
    setFlipped(false)
    setDone(0)
    setLastResult(null)
    api
      .dueCards({ all: includeAll })
      .then((data) => {
        setQueue(data.cards)
        setGoal(data.daily_goal)
        setReviewedToday(data.reviewed_today)
        setDueTotal(data.due_total)
      })
      .catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    load()
  }, [load])
  useEffect(() => stopSpeaking, []) // silencia ao sair da tela

  function toggleMute() {
    setMuted((current) => {
      const next = !current
      try {
        localStorage.setItem(MUTE_KEY, next ? '1' : '0')
      } catch {
        /* storage bloqueado */
      }
      if (next) stopSpeaking()
      return next
    })
  }

  // Vira o cartão; ao revelar a resposta, fala o idioma estudado (salvo se mudo).
  function flip() {
    setFlipped((wasFlipped) => {
      const nowFlipped = !wasFlipped
      if (nowFlipped && !muted) speak(queue[0].back_target, queue[0].language)
      else stopSpeaking()
      return nowFlipped
    })
  }

  async function grade(value) {
    stopSpeaking()
    const card = queue[0]
    setSubmitting(true)
    try {
      const result = await api.submitReview(card.id, value)
      setLastResult(result)
      setDone((n) => n + 1)
      setQueue((current) => current.slice(1))
      setFlipped(false)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (error) return <ErrorState message={error} onRetry={load} />
  if (queue === null) return <Spinner label="Buscando cartões vencidos…" />

  if (queue.length === 0) {
    const studiedToday = reviewedToday + done
    const goalReached = goal > 0 && studiedToday >= goal
    const stillDue = Math.max(0, dueTotal - done)

    return (
      <EmptyState
        icon={goalReached ? '🎯' : '🎉'}
        title={goalReached ? 'Meta do dia batida!' : 'Fila zerada!'}
      >
        <p className="tabular-nums">
          {studiedToday}/{goal} cartões hoje
          {done > 0 && ` · ${done} nesta sessão`}.
        </p>
        <p className="mt-1">
          {stillDue > 0
            ? `Ainda há ${stillDue} ${stillDue === 1 ? 'cartão vencido' : 'cartões vencidos'} — pode parar por hoje ou seguir.`
            : 'Nada mais vencido agora.'}
        </p>
        <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
          {stillDue > 0 && !isGuest && (
            <Button onClick={() => load(true)}>Revisar mais (+{stillDue})</Button>
          )}
          <Link
            to="/dashboard"
            className="font-semibold text-accent-600 underline underline-offset-4 dark:text-accent-400"
          >
            Ver o dashboard →
          </Link>
        </div>
      </EmptyState>
    )
  }

  const card = queue[0]
  const studiedToday = reviewedToday + done
  const progress = goal ? Math.min(100, (studiedToday / goal) * 100) : 0

  return (
    <div>
      <div className="mb-6">
        <div className="mb-2 flex items-center justify-between text-xs font-medium text-zinc-500 dark:text-zinc-400">
          <span>{queue.length} na fila</span>
          <div className="flex items-center gap-3">
            <span className="tabular-nums">
              {studiedToday}/{goal} · meta
            </span>
            {speechSupported && !muted && (
              <button
                onClick={cycleSpeechRate}
                aria-label="Velocidade da voz"
                title="Velocidade da voz"
                className="rounded-lg px-1.5 py-1 font-semibold tabular-nums text-zinc-400 transition-colors hover:bg-zinc-100 hover:text-zinc-700 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
              >
                {speechRate}×
              </button>
            )}
            {speechSupported && (
              <button
                onClick={toggleMute}
                aria-label={muted ? 'Ativar voz' : 'Desativar voz'}
                className="grid size-7 place-items-center rounded-lg text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 dark:hover:bg-zinc-800 dark:hover:text-zinc-200"
              >
                {muted ? <SpeakerOffIcon className="size-4" /> : <SpeakerIcon className="size-4" />}
              </button>
            )}
          </div>
        </div>
        <div className="h-1.5 overflow-hidden rounded-full bg-zinc-200 dark:bg-zinc-800">
          <div
            className="h-full rounded-full bg-accent-500 transition-[width] duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {lastResult && (
        <p className="animate-rise mb-4 rounded-xl bg-zinc-100 px-3 py-2 text-sm text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
          +{lastResult.points_earned} pts · próxima revisão {nextIntervalLabel(lastResult.new_interval)}
        </p>
      )}

      <Flashcard
        card={card}
        flipped={flipped}
        onFlip={flip}
        onSpeak={() => speak(card.back_target, card.language)}
      />

      <div className="mt-6">
        {!flipped ? (
          <Button onClick={flip} className="w-full">
            Mostrar resposta
          </Button>
        ) : isGuest ? (
          <p className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-center text-sm text-amber-700 dark:border-amber-900/60 dark:bg-amber-950/40 dark:text-amber-300">
            Visitante não pode revisar. Entre com uma conta para pontuar.
          </p>
        ) : (
          <>
            <p className="mb-2 text-center text-sm text-zinc-500 dark:text-zinc-400">
              Quão bem você lembrou?
            </p>
            <div className="grid grid-cols-3 gap-2 sm:grid-cols-6">
              {GRADES.map((option) => (
                <button
                  key={option.value}
                  disabled={submitting}
                  onClick={() => grade(option.value)}
                  className={`flex flex-col items-center gap-0.5 rounded-xl border bg-white px-2 py-3 text-[11px] font-semibold transition-colors disabled:opacity-40 dark:bg-zinc-900 ${TONE[option.tone]}`}
                >
                  <span className="text-lg">{option.value}</span>
                  {option.label}
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
