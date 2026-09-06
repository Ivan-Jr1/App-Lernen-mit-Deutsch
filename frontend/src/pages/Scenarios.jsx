import { useCallback, useEffect, useState } from 'react'

import { api } from '../api.js'
import { EmptyState, ErrorBox, Loading } from '../components/States.jsx'
import { useUser } from '../user.jsx'

function ScenarioList({ scenarios, onPick }) {
  if (scenarios.length === 0) return <EmptyState>Nenhum cenário cadastrado.</EmptyState>
  return (
    <ul className="space-y-3">
      {scenarios.map((scenario) => (
        <li key={scenario.slug}>
          <button
            onClick={() => onPick(scenario.slug)}
            className="w-full rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-slate-300"
          >
            <span className="text-xs font-medium uppercase tracking-wide text-slate-400">
              {scenario.category}
            </span>
            <p className="mt-1 font-semibold text-slate-900">{scenario.title}</p>
            <p className="mt-1 text-sm text-slate-500">{scenario.description}</p>
          </button>
        </li>
      ))}
    </ul>
  )
}

function Player({ scenario, username, onExit }) {
  const [attemptId, setAttemptId] = useState(null)
  const [stepIndex, setStepIndex] = useState(0)
  const [answer, setAnswer] = useState(null) // resultado do passo atual
  const [summary, setSummary] = useState(null) // preenchido ao ver o resultado final
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    api
      .startAttempt(username, scenario.slug)
      .then((attempt) => setAttemptId(attempt.id))
      .catch((err) => setError(err.message))
  }, [username, scenario.slug])

  const step = scenario.steps[stepIndex]

  async function choose(optionId) {
    setBusy(true)
    try {
      const result = await api.answerStep(username, attemptId, step.id, optionId)
      setAnswer({ ...result, chosenOptionId: optionId })
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function advance() {
    if (answer?.attempt_completed) {
      setSummary(await api.getAttempt(username, attemptId))
      return
    }
    setStepIndex((index) => index + 1)
    setAnswer(null)
  }

  if (error) return <ErrorBox message={error} onRetry={onExit} />
  if (!attemptId) return <Loading label="Iniciando cenário…" />

  if (summary) {
    return (
      <EmptyState>
        <p className="text-lg font-semibold text-slate-700">Cenário concluído ✅</p>
        <p className="mt-1 text-sm">
          {summary.correct_count} de {summary.total_steps} na primeira tentativa · +
          {summary.points_earned} pontos
        </p>
        <button
          onClick={onExit}
          className="mt-4 text-sm font-medium text-slate-900 underline underline-offset-2"
        >
          Voltar aos cenários
        </button>
      </EmptyState>
    )
  }

  return (
    <div>
      <button onClick={onExit} className="mb-4 text-sm text-slate-500 hover:text-slate-700">
        ← Sair
      </button>

      <p className="mb-1 text-xs font-medium uppercase tracking-wide text-slate-400">
        Passo {stepIndex + 1} de {scenario.steps.length}
      </p>

      <div className="rounded-2xl bg-slate-800 p-5 text-white">
        <p className="text-xs text-slate-400">Atendente</p>
        <p className="mt-1 text-lg font-medium">{step.speaker_text_de}</p>
        {step.speaker_text_pt && (
          <p className="mt-1 text-sm text-slate-400">{step.speaker_text_pt}</p>
        )}
      </div>

      <div className="mt-4 space-y-2">
        {step.options.map((option) => {
          const isChosen = answer?.chosenOptionId === option.id
          const isCorrect = answer?.correct_option_id === option.id
          let style = 'border-slate-200 bg-white hover:border-slate-300'
          if (answer) {
            if (isCorrect) style = 'border-emerald-300 bg-emerald-50'
            else if (isChosen) style = 'border-red-300 bg-red-50'
            else style = 'border-slate-200 bg-white opacity-60'
          }
          return (
            <button
              key={option.id}
              disabled={Boolean(answer) || busy}
              onClick={() => choose(option.id)}
              className={`w-full rounded-lg border px-4 py-3 text-left text-sm transition disabled:cursor-default ${style}`}
            >
              {option.option_text_de}
            </button>
          )
        })}
      </div>

      {answer && (
        <div className="mt-4">
          <p
            className={`text-sm font-semibold ${
              answer.is_correct ? 'text-emerald-700' : 'text-red-700'
            }`}
          >
            {answer.is_correct ? 'Boa!' : 'Não é a mais natural.'}
          </p>
          <p className="mt-1 text-sm text-slate-600">{answer.explanation}</p>
          <button
            onClick={advance}
            className="mt-3 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          >
            {answer.attempt_completed ? 'Ver resultado' : 'Próximo'}
          </button>
        </div>
      )}
    </div>
  )
}

export default function Scenarios() {
  const { username } = useUser()
  const [scenarios, setScenarios] = useState(null)
  const [error, setError] = useState(null)
  const [active, setActive] = useState(null) // cenário detalhado em andamento

  const loadList = useCallback(() => {
    setError(null)
    setActive(null)
    api.listScenarios().then(setScenarios).catch((err) => setError(err.message))
  }, [])

  useEffect(loadList, [loadList])

  function pick(slug) {
    setError(null)
    api.getScenario(slug).then(setActive).catch((err) => setError(err.message))
  }

  if (error) return <ErrorBox message={error} onRetry={loadList} />
  if (active) return <Player scenario={active} username={username} onExit={loadList} />
  if (scenarios === null) return <Loading />
  return <ScenarioList scenarios={scenarios} onPick={pick} />
}
