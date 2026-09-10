import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext.jsx'
import { api } from '../lib/api.js'
import { LogoMark } from '../components/Logo.jsx'
import { Button, Spinner } from '../components/ui.jsx'

export default function Login() {
  const navigate = useNavigate()
  const { login, claim, guest } = useAuth()

  const [accounts, setAccounts] = useState(null)
  const [picked, setPicked] = useState(null) // conta selecionada
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    api.accounts().then(setAccounts).catch((err) => setError(err.message))
  }, [])

  const isClaiming = picked && !picked.claimed

  async function submit(event) {
    event.preventDefault()
    setError(null)
    if (isClaiming && password !== confirm) {
      setError('As senhas não conferem.')
      return
    }
    setBusy(true)
    try {
      if (isClaiming) await claim(picked.username, password)
      else await login(picked.username, password)
      navigate('/welcome', { replace: true }) // passo de idioma antes do app
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function enterAsGuest() {
    setBusy(true)
    try {
      await guest()
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
          <h1 className="mt-4 text-2xl font-bold tracking-tight">Learning Languages</h1>
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            Alemão e inglês, um cartão de cada vez
          </p>
        </div>

        <div className="animate-rise rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          {accounts === null && !error && <Spinner label="Carregando…" />}

          {accounts && !picked && (
            <div className="space-y-2">
              <p className="mb-3 text-sm font-medium text-zinc-500 dark:text-zinc-400">
                Quem é você?
              </p>
              {accounts.map((account) => (
                <button
                  key={account.username}
                  onClick={() => {
                    setPicked(account)
                    setError(null)
                  }}
                  className="flex w-full items-center justify-between rounded-xl border border-zinc-200 px-4 py-3 text-left transition-colors hover:border-indigo-400 hover:bg-indigo-50/50 dark:border-zinc-700 dark:hover:border-indigo-500 dark:hover:bg-indigo-950/30"
                >
                  <span className="flex items-center gap-3">
                    <span className="grid size-9 place-items-center rounded-full bg-zinc-100 text-sm font-bold text-zinc-600 dark:bg-zinc-800 dark:text-zinc-200">
                      {account.display_name[0]}
                    </span>
                    <span className="font-semibold">{account.display_name}</span>
                  </span>
                  <span className="text-xs text-zinc-400">
                    {account.claimed ? 'entrar' : 'criar senha'}
                  </span>
                </button>
              ))}
            </div>
          )}

          {picked && (
            <form onSubmit={submit} className="space-y-4">
              <button
                type="button"
                onClick={() => {
                  setPicked(null)
                  setPassword('')
                  setConfirm('')
                  setError(null)
                }}
                className="text-sm text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-100"
              >
                ← {picked.display_name}
              </button>

              <div>
                <label className="text-sm font-medium" htmlFor="password">
                  {isClaiming ? 'Crie uma senha' : 'Senha'}
                </label>
                <input
                  id="password"
                  type="password"
                  autoFocus
                  autoComplete={isClaiming ? 'new-password' : 'current-password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="mt-1 w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-zinc-700"
                />
              </div>

              {isClaiming && (
                <div>
                  <label className="text-sm font-medium" htmlFor="confirm">
                    Repita a senha
                  </label>
                  <input
                    id="confirm"
                    type="password"
                    autoComplete="new-password"
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    className="mt-1 w-full rounded-xl border border-zinc-300 bg-transparent px-3 py-2.5 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 dark:border-zinc-700"
                  />
                </div>
              )}

              {isClaiming && (
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  Primeiro acesso desta conta — a senha que você definir agora fica valendo.
                </p>
              )}

              <Button type="submit" disabled={busy || password.length < 6} className="w-full">
                {busy ? 'Aguarde…' : isClaiming ? 'Criar senha e entrar' : 'Entrar'}
              </Button>
            </form>
          )}

          {error && (
            <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">
              {error}
            </p>
          )}
        </div>

        <button
          onClick={enterAsGuest}
          disabled={busy}
          className="mt-4 w-full text-center text-sm text-zinc-500 underline underline-offset-4 hover:text-zinc-800 disabled:opacity-50 dark:hover:text-zinc-100"
        >
          Entrar como visitante (somente leitura)
        </button>
      </div>
    </div>
  )
}
