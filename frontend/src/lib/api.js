// Cliente HTTP fino sobre o fetch.
//
// Em dev, BASE é vazio e as chamadas caem em /api/... (repassadas pelo proxy do
// Vite). Em produção, defina VITE_API_URL com a URL pública do backend.
//
// O token e o tratamento de 401 são injetados pelo AuthContext via os setters
// abaixo, para o cliente não depender do React.

const BASE = import.meta.env.VITE_API_URL ?? ''

let authToken = null
let handleUnauthorized = () => {}

export function setAuthToken(token) {
  authToken = token
}

export function setUnauthorizedHandler(handler) {
  handleUnauthorized = handler
}

async function request(path, { authenticated = true, ...options } = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  if (authenticated && authToken) headers.Authorization = `Bearer ${authToken}`

  const response = await fetch(`${BASE}${path}`, { ...options, headers })

  if (response.status === 401) {
    handleUnauthorized()
    throw new Error('Sua sessão expirou. Entre novamente.')
  }
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}))
    throw new Error(detail.detail || `Erro ${response.status}`)
  }
  return response.status === 204 ? null : response.json()
}

export const api = {
  // Autenticação (sem token)
  accounts: () => request('/api/auth/accounts', { authenticated: false }),
  claim: (username, password) =>
    request('/api/auth/claim', {
      authenticated: false,
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  login: (username, password) =>
    request('/api/auth/login', {
      authenticated: false,
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  guest: () => request('/api/auth/guest', { authenticated: false, method: 'POST' }),
  updateProfile: (patch) =>
    request('/api/auth/me', { method: 'PATCH', body: JSON.stringify(patch) }),
  changePassword: (currentPassword, newPassword) =>
    request('/api/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    }),

  // Flashcards
  dueCards: (limit = 60) => request(`/api/reviews/due?limit=${limit}`),
  submitReview: (cardId, grade) =>
    request('/api/reviews', {
      method: 'POST',
      body: JSON.stringify({ card_id: cardId, grade }),
    }),

  // Cenários
  listScenarios: () => request('/api/scenarios'),
  getScenario: (slug) => request(`/api/scenarios/${slug}`),
  startAttempt: (slug) => request(`/api/scenarios/${slug}/attempts`, { method: 'POST' }),
  answerStep: (attemptId, stepId, optionId) =>
    request(`/api/attempts/${attemptId}/answers`, {
      method: 'POST',
      body: JSON.stringify({ step_id: stepId, option_id: optionId }),
    }),
  getAttempt: (attemptId) => request(`/api/attempts/${attemptId}`),

  // Dashboard
  dashboard: () => request('/api/dashboard'),
}
