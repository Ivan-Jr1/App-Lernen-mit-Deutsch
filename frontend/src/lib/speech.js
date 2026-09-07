// Fala em alemão via Web Speech API do navegador — sem backend, sem custo.
// A qualidade da voz depende do sistema (boa no Android/iOS; varia no desktop).

export const speechSupported =
  typeof window !== 'undefined' && 'speechSynthesis' in window

let germanVoice = null

function resolveGermanVoice() {
  if (germanVoice) return germanVoice
  const voices = window.speechSynthesis.getVoices()
  germanVoice =
    voices.find((v) => v.lang === 'de-DE') ||
    voices.find((v) => v.lang?.startsWith('de')) ||
    null
  return germanVoice
}

if (speechSupported) {
  // A lista de vozes chega de forma assíncrona em alguns navegadores.
  window.speechSynthesis.addEventListener('voiceschanged', () => {
    germanVoice = null
    resolveGermanVoice()
  })
  resolveGermanVoice()
}

export function speakGerman(text) {
  if (!speechSupported || !text) return
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'de-DE'
  utterance.rate = 0.95
  const voice = resolveGermanVoice()
  if (voice) utterance.voice = voice
  window.speechSynthesis.speak(utterance)
}

export function stopSpeaking() {
  if (speechSupported) window.speechSynthesis.cancel()
}
