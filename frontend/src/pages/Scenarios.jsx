import { useCallback, useEffect, useState } from 'react'

import { useAuth } from '../auth/AuthContext.jsx'
import { api } from '../lib/api.js'
import { speak, speechSupported } from '../lib/speech.js'
import { languageName } from '../lib/languages.js'
import { SpeakerIcon } from '../components/icons.jsx'
import { Button, Card, EmptyState, ErrorState, Spinner } from '../components/ui.jsx'

function ScenarioList({ scenarios, onPick }) {
  if (scenarios.length === 0) return <EmptyState icon="📋" title="Nenhum cenário cadastrado." />
  return (
    <ul className="space-y-3">
      {scenarios.map((scenario) => (
        <li key={scenario.slug}>
          <button
            onClick={() => onPick(scenario.slug)}
            className="group w-full rounded-2xl border border-zinc-200 bg-white p-5 text-left shadow-sm transition-colors hover:border-accent-400 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-accent-500"
          >
            <span className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
              {scenario.category}
            </span>
            <p className="mt-1 font-semibold text-zinc-900 group-hover:text-accent-600 dark:text-zinc-50 dark:group-hover:text-accent-400">
              {scenario.title}
            </p>
            <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">{scenario.description}</p>
          </button>
        </li>
      ))}
    </ul>
  )
}

function optionStyle(answer, option) {
  if (!answer) return 'border-zinc-200 bg-white hover:border-accent-400 dark:border-zinc-700 dark:bg-zinc-900'
  if (option.id === answer.correct_option_id)
    return 'border-emerald-300 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-950/40'
  if (option.id === answer.chosenOptionId)
    return 'border-rose-300 bg-rose-50 dark:border-rose-800 dark:bg-rose-950/40'
  return 'border-zinc-200 bg-white opacity-50 dark:border-zinc-800 dark:bg-zinc-900'
}

function Player({ scenario, onExit }) {
  const [attemptId, setAttemptId] = useState(null)
  const [stepIndex, setStepIndex] = useState(0)
  const [answer, setAnswer] = useState(null)
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    api
      .startAttempt(scenario.slug)
      .then((attempt) => setAttemptId(attempt.id))
      .catch((err) => setError(err.message))
  }, [scenario.slug])

  const step = scenario.steps[stepIndex]

  async function choose(optionId) {
    setBusy(true)
    try {
      const result = await api.answerStep(attemptId, step.id, optionId)
      setAnswer({ ...result, chosenOptionId: optionId })
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function advance() {
    if (answer?.attempt_completed) {
      setSummary(await api.getAttempt(attemptId))
      return
    }
    setStepIndex((index) => index + 1)
    setAnswer(null)
  }

  if (error) return <ErrorState message={error} onRetry={onExit} />
  if (!attemptId) return <Spinner label="Iniciando cenário…" />

  if (summary) {
    const flawless = summary.correct_count === summary.total_steps
    return (
      <EmptyState icon={flawless ? '🏆' : '✅'} title="Cenário concluído">
        {summary.correct_count} de {summary.total_steps} na primeira tentativa · +
        {summary.points_earned} pontos
        <div className="mt-4">
          <Button variant="secondary" onClick={onExit}>
            Voltar aos cenários
          </Button>
        </div>
      </EmptyState>
    )
  }

  return (
    <div>
      <button
        onClick={onExit}
        className="mb-4 text-sm text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-100"
      >
        ← Sair
      </button>

      <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-zinc-400">
        Passo {stepIndex + 1} de {scenario.steps.length}
      </p>

      <div className="max-w-[85%] rounded-2xl rounded-tl-sm bg-zinc-800 p-4 text-white dark:bg-zinc-800">
        <div className="flex items-center justify-between">
          <p className="text-xs text-zinc-400">Atendente</p>
          {speechSupported && (
            <button
              onClick={() => speak(step.speaker_text_target, scenario.language)}
              aria-label={`Ouvir em ${languageName(scenario.language)}`}
              className="grid size-7 place-items-center rounded-full bg-white/10 hover:bg-white/20"
            >
              <SpeakerIcon className="size-4" />
            </button>
          )}
        </div>
        <p className="mt-1 font-medium">{step.speaker_text_target}</p>
        {step.speaker_text_pt && (
          <p className="mt-1 text-sm text-zinc-400">{step.speaker_text_pt}</p>
        )}
      </div>

      <div className="mt-4 space-y-2">
        {step.options.map((option) => (
          <button
            key={option.id}
            disabled={Boolean(answer) || busy}
            onClick={() => choose(option.id)}
            className={`w-full rounded-xl border px-4 py-3 text-left text-sm transition-colors disabled:cursor-default ${optionStyle(answer, option)}`}
          >
            {option.option_text_target}
          </button>
        ))}
      </div>

      {answer && (
        <Card className="animate-rise mt-4 p-4">
          <p
            className={`text-sm font-semibold ${
              answer.is_correct
                ? 'text-emerald-600 dark:text-emerald-400'
                : 'text-rose-600 dark:text-rose-400'
            }`}
          >
            {answer.is_correct ? 'Boa! Resposta natural.' : 'Não é a mais natural.'}
          </p>
          <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-300">{answer.explanation}</p>
          <Button onClick={advance} className="mt-3">
            {answer.attempt_completed ? 'Ver resultado' : 'Próximo'}
          </Button>
        </Card>
      )}
    </div>
  )
}

export default function Scenarios() {
  const { isGuest } = useAuth()
  const [scenarios, setScenarios] = useState(null)
  const [error, setError] = useState(null)
  const [active, setActive] = useState(null)

  const loadList = useCallback(() => {
    setError(null)
    setActive(null)
    api.listScenarios().then(setScenarios).catch((err) => setError(err.message))
  }, [])

  useEffect(loadList, [loadList])

  function pick(slug) {
    if (isGuest) {
      setError('Visitante não pode jogar os cenários. Entre com uma conta.')
      return
    }
    setError(null)
    api.getScenario(slug).then(setActive).catch((err) => setError(err.message))
  }

  if (error && !active && scenarios) {
    return (
      <div className="space-y-4">
        <ErrorState message={error} onRetry={loadList} />
        <ScenarioList scenarios={scenarios} onPick={pick} />
      </div>
    )
  }
  if (error) return <ErrorState message={error} onRetry={loadList} />
  if (active) return <Player scenario={active} onExit={loadList} />
  if (scenarios === null) return <Spinner />
  return <ScenarioList scenarios={scenarios} onPick={pick} />
}
