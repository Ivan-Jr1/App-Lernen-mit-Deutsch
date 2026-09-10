import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext.jsx'
import { api } from '../lib/api.js'
import { LANGUAGE_OPTIONS } from '../lib/languages.js'
import { LogoMark } from '../components/Logo.jsx'
import { Button, Spinner } from '../components/ui.jsx'
import { CheckIcon } from '../components/icons.jsx'

// Passo logo após o login/cadastro: confirmar ou trocar o idioma de estudo da
// sessão. O idioma atual já vem selecionado, então quase sempre é um clique.
export default function Welcome() {
  const navigate = useNavigate()
  const { user, updateUser } = useAuth()

  const [languages, setLanguages] = useState(null)
  const [selected, setSelected] = useState(user?.learning_language ?? 'de')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    api
      .listLanguages()
      .then(setLanguages)
      .catch(() => setLanguages(LANGUAGE_OPTIONS)) // API fria: segue com a lista local
  }, [])

  async function start() {
    setBusy(true)
    setError(null)
    try {
      if (selected !== user.learning_language) {
        const updated = await api.updateProfile({ learning_language: selected })
        updateUser(updated)
      }
      navigate('/review', { replace: true })
    } catch (err) {
      setError(err.message)
      setBusy(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-zinc-50 to-zinc-100 px-4 dark:from-zinc-950 dark:to-zinc-900">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <LogoMark className="mx-auto size-14 rounded-2xl" />
          <h1 className="mt-4 text-2xl font-bold tracking-tight">
            O que vamos estudar hoje?
          </h1>
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            Dá pra trocar quando quiser nas configurações.
          </p>
        </div>

        <div className="animate-rise rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          {languages === null ? (
            <Spinner label="Carregando…" />
          ) : (
            <>
              <div className="grid grid-cols-2 gap-3">
                {languages.map((language) => {
                  const active = language.code === selected
                  return (
                    <button
                      key={language.code}
                      onClick={() => setSelected(language.code)}
                      className={`flex flex-col items-center gap-2 rounded-xl border px-3 py-5 text-sm font-semibold transition-colors ${
                        active
                          ? 'border-accent-500 bg-accent-50 text-accent-700 dark:bg-accent-950/50 dark:text-accent-300'
                          : 'border-zinc-200 bg-white text-zinc-600 hover:border-accent-400 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-300'
                      }`}
                    >
                      {language.name}
                      <span
                        className={`grid size-5 place-items-center rounded-full ${
                          active ? 'bg-accent-600 text-white' : 'bg-zinc-100 dark:bg-zinc-800'
                        }`}
                      >
                        {active && <CheckIcon className="size-3.5" />}
                      </span>
                    </button>
                  )
                })}
              </div>

              <Button onClick={start} disabled={busy} className="mt-5 w-full">
                {busy ? 'Aguarde…' : 'Continuar'}
              </Button>
            </>
          )}

          {error && (
            <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
