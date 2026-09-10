import { useEffect, useRef, useState } from 'react'

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
import {
  CameraIcon,
  CheckIcon,
  ChartIcon,
  GlobeIcon,
  LockIcon,
  SpeakerIcon,
  TrashIcon,
  UserIcon,
} from '../components/icons.jsx'
import { Avatar, Button, Card, EmptyState } from '../components/ui.jsx'

// Redimensiona a imagem no cliente para 256x256 (corte central) e devolve um
// data URI JPEG — mantém a foto pequena o bastante para caber numa coluna do banco.
function resizeToDataUrl(file, size = 256) {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = canvas.height = size
      const ctx = canvas.getContext('2d')
      const scale = Math.max(size / image.width, size / image.height)
      const w = image.width * scale
      const h = image.height * scale
      ctx.drawImage(image, (size - w) / 2, (size - h) / 2, w, h)
      URL.revokeObjectURL(image.src)
      resolve(canvas.toDataURL('image/jpeg', 0.82))
    }
    image.onerror = reject
    image.src = URL.createObjectURL(file)
  })
}

function Feedback({ state }) {
  if (!state) return null
  const isError = state.type === 'error'
  return (
    <p
      className={`mt-3 flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm ${
        isError
          ? 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-300'
          : 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300'
      }`}
    >
      {!isError && <CheckIcon className="size-4" />}
      {state.message}
    </p>
  )
}

function ProfileCard() {
  const { user, updateUser } = useAuth()
  const fileInput = useRef(null)
  const [name, setName] = useState(user.display_name)
  const [avatar, setAvatar] = useState(user.avatar_url ?? null)
  const [goal, setGoal] = useState(user.daily_goal)
  const [saving, setSaving] = useState(false)
  const [feedback, setFeedback] = useState(null)

  const goalValid = Number.isInteger(goal) && goal >= 1 && goal <= 200
  const dirty =
    name !== user.display_name ||
    avatar !== (user.avatar_url ?? null) ||
    goal !== user.daily_goal

  async function pickPhoto(event) {
    const file = event.target.files?.[0]
    if (!file) return
    setFeedback(null)
    if (file.size > 8_000_000) {
      setFeedback({ type: 'error', message: 'Imagem muito grande (máx. 8 MB).' })
      return
    }
    try {
      setAvatar(await resizeToDataUrl(file))
    } catch {
      setFeedback({ type: 'error', message: 'Não consegui ler essa imagem.' })
    }
  }

  async function save() {
    setSaving(true)
    setFeedback(null)
    try {
      const updated = await api.updateProfile({
        display_name: name,
        avatar_url: avatar,
        daily_goal: goal,
      })
      updateUser(updated)
      setFeedback({ type: 'ok', message: 'Perfil salvo.' })
    } catch (err) {
      setFeedback({ type: 'error', message: err.message })
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card className="p-5">
      <h2 className="flex items-center gap-2 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
        <UserIcon className="size-4" /> Perfil
      </h2>

      <div className="mt-4 flex items-center gap-4">
        <div className="relative">
          <Avatar src={avatar} name={name} className="size-20 text-2xl" />
          <button
            onClick={() => fileInput.current?.click()}
            className="absolute -bottom-1 -right-1 grid size-8 place-items-center rounded-full bg-indigo-600 text-white ring-2 ring-white hover:bg-indigo-500 dark:ring-zinc-900"
            aria-label="Trocar foto"
          >
            <CameraIcon className="size-4" />
          </button>
          <input
            ref={fileInput}
            type="file"
            accept="image/*"
            hidden
            onChange={pickPhoto}
          />
        </div>
        {avatar && (
          <button
            onClick={() => setAvatar(null)}
            className="flex items-center gap-1.5 text-sm text-zinc-500 hover:text-red-600"
          >
            <TrashIcon className="size-4" /> Remover foto
          </button>
        )}
      </div>

      <label className="mt-5 block text-sm font-medium" htmlFor="display_name">
        Nome de exibição
      </label>
      <input
        id="display_name"
        value={name}
        maxLength={60}
        onChange={(e) => setName(e.target.value)}
        className="mt-1 w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-zinc-700"
      />

      <label className="mt-5 block text-sm font-medium" htmlFor="daily_goal">
        Meta diária de cartões
      </label>
      <p className="text-xs text-zinc-500 dark:text-zinc-400">
        A fila de revisão para nesse número por dia. Dá pra continuar além dela quando quiser.
      </p>
      <input
        id="daily_goal"
        type="number"
        inputMode="numeric"
        min={1}
        max={200}
        value={Number.isNaN(goal) ? '' : goal}
        onChange={(e) => setGoal(parseInt(e.target.value, 10))}
        className="mt-1 w-24 rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-zinc-700"
      />

      <Button
        onClick={save}
        disabled={!dirty || saving || !name.trim() || !goalValid}
        className="mt-4"
      >
        {saving ? 'Salvando…' : 'Salvar perfil'}
      </Button>
      <Feedback state={feedback} />
    </Card>
  )
}

function PasswordCard() {
  const [current, setCurrent] = useState('')
  const [next, setNext] = useState('')
  const [confirm, setConfirm] = useState('')
  const [saving, setSaving] = useState(false)
  const [feedback, setFeedback] = useState(null)

  async function submit(event) {
    event.preventDefault()
    setFeedback(null)
    if (next !== confirm) {
      setFeedback({ type: 'error', message: 'A nova senha e a confirmação não conferem.' })
      return
    }
    setSaving(true)
    try {
      await api.changePassword(current, next)
      setCurrent('')
      setNext('')
      setConfirm('')
      setFeedback({ type: 'ok', message: 'Senha alterada.' })
    } catch (err) {
      setFeedback({ type: 'error', message: err.message })
    } finally {
      setSaving(false)
    }
  }

  const field =
    'mt-1 w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-zinc-700'

  return (
    <Card className="p-5">
      <h2 className="flex items-center gap-2 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
        <LockIcon className="size-4" /> Senha
      </h2>
      <form onSubmit={submit} className="mt-4 space-y-3">
        <div>
          <label className="text-sm font-medium" htmlFor="current">Senha atual</label>
          <input id="current" type="password" autoComplete="current-password"
            value={current} onChange={(e) => setCurrent(e.target.value)} className={field} />
        </div>
        <div>
          <label className="text-sm font-medium" htmlFor="new">Nova senha</label>
          <input id="new" type="password" autoComplete="new-password"
            value={next} onChange={(e) => setNext(e.target.value)} className={field} />
        </div>
        <div>
          <label className="text-sm font-medium" htmlFor="confirm">Repita a nova senha</label>
          <input id="confirm" type="password" autoComplete="new-password"
            value={confirm} onChange={(e) => setConfirm(e.target.value)} className={field} />
        </div>
        <Button
          type="submit"
          disabled={saving || !current || next.length < 6}
        >
          {saving ? 'Alterando…' : 'Alterar senha'}
        </Button>
        <Feedback state={feedback} />
      </form>
    </Card>
  )
}

function ResetScoreCard() {
  const [confirming, setConfirming] = useState(false)
  const [saving, setSaving] = useState(false)
  const [feedback, setFeedback] = useState(null)

  async function reset() {
    setSaving(true)
    setFeedback(null)
    try {
      await api.resetScore()
      setConfirming(false)
      setFeedback({ type: 'ok', message: 'Placar zerado. Os cartões que você aprendeu continuam agendados.' })
    } catch (err) {
      setFeedback({ type: 'error', message: err.message })
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card className="border-amber-200 p-5 dark:border-amber-900/50">
      <h2 className="flex items-center gap-2 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
        <ChartIcon className="size-4" /> Placar
      </h2>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
        Zera seus pontos, streak, cartões revisados e cenários completados. A agenda
        de revisão (SM-2) é mantida — você não perde o que já aprendeu. Só afeta a sua conta.
      </p>

      {confirming ? (
        <div className="mt-4 flex flex-wrap gap-2">
          <Button onClick={reset} disabled={saving} className="bg-red-600 hover:bg-red-500">
            {saving ? 'Zerando…' : 'Sim, zerar meu placar'}
          </Button>
          <Button variant="secondary" onClick={() => setConfirming(false)} disabled={saving}>
            Cancelar
          </Button>
        </div>
      ) : (
        <Button variant="secondary" onClick={() => setConfirming(true)} className="mt-4">
          Zerar meu placar
        </Button>
      )}
      <Feedback state={feedback} />
    </Card>
  )
}

// Exemplo curto para o usuário ouvir a diferença ao trocar a velocidade.
const VOICE_SAMPLES = {
  de: 'Guten Tag! Ich möchte mich anmelden.',
  en: 'Hello! I would like to check in, please.',
}

function LanguageCard() {
  const { user, updateUser } = useAuth()
  const [languages, setLanguages] = useState(null)
  const [saving, setSaving] = useState(null) // código sendo salvo
  const [feedback, setFeedback] = useState(null)

  useEffect(() => {
    api.listLanguages().then(setLanguages).catch(() => setLanguages([]))
  }, [])

  async function choose(code) {
    if (code === user.learning_language) return
    setSaving(code)
    setFeedback(null)
    try {
      const updated = await api.updateProfile({ learning_language: code })
      updateUser(updated)
      setFeedback({ type: 'ok', message: `Agora estudando ${languageName(code)}.` })
    } catch (err) {
      setFeedback({ type: 'error', message: err.message })
    } finally {
      setSaving(null)
    }
  }

  return (
    <Card className="p-5">
      <h2 className="flex items-center gap-2 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
        <GlobeIcon className="size-4" /> Idioma de estudo
      </h2>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
        Define os flashcards e cenários que aparecem, e a voz usada para falá-los.
        Seu progresso e a agenda de revisão de cada idioma são guardados separadamente.
      </p>

      <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-3">
        {(languages ?? []).map((language) => (
          <button
            key={language.code}
            onClick={() => choose(language.code)}
            disabled={saving !== null}
            className={`rounded-xl border px-2 py-3 text-sm font-semibold transition-colors disabled:opacity-50 ${
              language.code === user.learning_language
                ? 'border-indigo-500 bg-indigo-50 text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-300'
                : 'border-zinc-200 bg-white text-zinc-600 hover:border-indigo-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300'
            }`}
          >
            {saving === language.code ? 'Trocando…' : language.name}
          </button>
        ))}
      </div>
      <Feedback state={feedback} />
    </Card>
  )
}

function VoiceCard() {
  const { user } = useAuth()
  const [rate, setRate] = useState(getSpeechRate)
  const sample = VOICE_SAMPLES[user.learning_language] ?? VOICE_SAMPLES.de

  useEffect(() => stopSpeaking, []) // silencia ao sair da tela

  function choose(value) {
    setSpeechRate(value)
    setRate(value)
    speak(sample, user.learning_language) // toca um exemplo na nova velocidade
  }

  return (
    <Card className="p-5">
      <h2 className="flex items-center gap-2 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
        <SpeakerIcon className="size-4" /> Voz
      </h2>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
        Velocidade da fala em {languageName(user.learning_language)} nos flashcards e cenários.
      </p>

      {speechSupported ? (
        <>
          <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-4">
            {SPEECH_SPEED_PRESETS.map((speed) => (
              <button
                key={speed.value}
                onClick={() => choose(speed.value)}
                className={`rounded-xl border px-2 py-3 text-xs font-semibold transition-colors ${
                  rate === speed.value
                    ? 'border-indigo-500 bg-indigo-50 text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-300'
                    : 'border-zinc-200 bg-white text-zinc-600 hover:border-indigo-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300'
                }`}
              >
                {speed.label}
              </button>
            ))}
          </div>
          <button
            onClick={() => speak(sample, user.learning_language)}
            className="mt-3 text-sm font-medium text-indigo-600 underline underline-offset-4 hover:opacity-80 dark:text-indigo-400"
          >
            Ouvir exemplo de novo
          </button>
        </>
      ) : (
        <p className="mt-3 text-sm text-zinc-400">
          Este navegador não tem síntese de voz disponível.
        </p>
      )}
    </Card>
  )
}

export default function Settings() {
  const { isGuest } = useAuth()

  if (isGuest) {
    return (
      <EmptyState icon="👀" title="Modo visitante">
        Sem conta própria não há o que configurar. Entre como Ivan ou Gabriela.
      </EmptyState>
    )
  }

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold tracking-tight">Configurações</h1>
      <ProfileCard />
      <LanguageCard />
      <VoiceCard />
      <PasswordCard />
      <ResetScoreCard />
    </div>
  )
}
