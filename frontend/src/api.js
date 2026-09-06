// Cliente HTTP fino sobre o fetch. Em dev, BASE é vazio e as chamadas caem em
// /api/... (repassadas pelo proxy do Vite). Em produção, defina VITE_API_URL
// com a URL pública do backend no Render.
const BASE = import.meta.env.VITE_API_URL ?? ''

async function request(path, { user, ...options } = {}) {
  const url = new URL(`${BASE}${path}`, window.location.origin)
  if (user) url.searchParams.set('user', user)

  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}))
    throw new Error(detail.detail || `Erro ${response.status}`)
  }
  return response.status === 204 ? null : response.json()
}

export const api = {
  // Flashcards
  dueCards: (user, limit = 20) =>
    request(`/api/reviews/due?limit=${limit}`, { user }),
  submitReview: (user, cardId, grade) =>
    request('/api/reviews', {
      user,
      method: 'POST',
      body: JSON.stringify({ card_id: cardId, grade }),
    }),

  // Cenários
  listScenarios: () => request('/api/scenarios'),
  getScenario: (slug) => request(`/api/scenarios/${slug}`),
  startAttempt: (user, slug) =>
    request(`/api/scenarios/${slug}/attempts`, { user, method: 'POST' }),
  answerStep: (user, attemptId, stepId, optionId) =>
    request(`/api/attempts/${attemptId}/answers`, {
      user,
      method: 'POST',
      body: JSON.stringify({ step_id: stepId, option_id: optionId }),
    }),
  getAttempt: (user, attemptId) => request(`/api/attempts/${attemptId}`, { user }),

  // Dashboard
  dashboard: () => request('/api/dashboard'),
}
