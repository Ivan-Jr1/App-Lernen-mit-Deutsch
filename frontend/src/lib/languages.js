// Nome dos idiomas de estudo, em minúsculas para uso inline
// (ex.: "Ouvir em inglês"). A lista completa vem de GET /api/languages.

export const LANGUAGE_NAMES = { de: 'alemão', en: 'inglês' }

export function languageName(code) {
  return LANGUAGE_NAMES[code] ?? code
}
