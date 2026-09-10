// Nome dos idiomas de estudo, em minúsculas para uso inline
// (ex.: "Ouvir em inglês"). A lista completa (com nome capitalizado) vem de
// GET /api/languages; LANGUAGE_OPTIONS é só o fallback se a API estiver fora.

export const LANGUAGE_NAMES = { de: 'alemão', en: 'inglês' }

export const LANGUAGE_OPTIONS = [
  { code: 'de', name: 'Alemão' },
  { code: 'en', name: 'Inglês' },
]

export function languageName(code) {
  return LANGUAGE_NAMES[code] ?? code
}
