// Estado de autenticação: token + usuário logado, persistidos no localStorage.
// Sem backend de sessão — o token JWT é a sessão.

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import { api, setAuthToken, setUnauthorizedHandler } from '../lib/api.js'

const STORAGE_KEY = 'deutsch-app:session'
const AuthContext = createContext(null)

function readStoredSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [session, setSession] = useState(readStoredSession)

  // Mantém o cliente HTTP em sincronia com o token atual.
  setAuthToken(session?.token ?? null)

  const persist = useCallback((next) => {
    setSession(next)
    setAuthToken(next?.token ?? null)
    try {
      if (next) localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      else localStorage.removeItem(STORAGE_KEY)
    } catch {
      /* modo privado / storage bloqueado — a sessão vive só em memória */
    }
  }, [])

  const logout = useCallback(() => persist(null), [persist])

  useEffect(() => {
    setUnauthorizedHandler(logout)
  }, [logout])

  const applyToken = useCallback(
    (tokenResponse) => {
      persist({ token: tokenResponse.access_token, user: tokenResponse.user })
      return tokenResponse.user
    },
    [persist],
  )

  // Atualiza os dados do usuário na sessão (nome/foto) sem mexer no token.
  const updateUser = useCallback(
    (patch) => {
      setSession((current) => {
        if (!current) return current
        const next = { ...current, user: { ...current.user, ...patch } }
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
        } catch {
          /* storage bloqueado */
        }
        return next
      })
    },
    [],
  )

  const value = useMemo(
    () => ({
      user: session?.user ?? null,
      isAuthenticated: Boolean(session?.token),
      isGuest: Boolean(session?.user?.readonly),
      login: async (username, password) => applyToken(await api.login(username, password)),
      claim: async (username, password) => applyToken(await api.claim(username, password)),
      guest: async () => applyToken(await api.guest()),
      updateUser,
      logout,
    }),
    [session, applyToken, updateUser, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth precisa estar dentro de <AuthProvider>')
  return context
}
