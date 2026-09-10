// Fala o idioma estudado via Web Speech API do navegador — sem backend, sem custo.
// A qualidade da voz depende do sistema, então para cada idioma escolhemos a
// melhor voz disponível e preparamos o texto para soar mais natural.

export const speechSupported =
  typeof window !== 'undefined' && 'speechSynthesis' in window

// Locale BCP-47 usado na fala, por código de idioma.
const LOCALES = { de: 'de-DE', en: 'en-US' }

// Vozes boas conhecidas por idioma, da melhor para a pior. Os nomes variam entre
// navegadores/SOs, então isto serve para pontuar o que o sistema oferecer.
const PREFERRED_VOICES = {
  de: ['Google Deutsch', 'Microsoft Katja', 'Microsoft Hedda', 'Anna', 'Petra', 'Helena', 'Markus'],
  en: [
    'Google US English',
    'Google UK English Female',
    'Microsoft Aria',
    'Microsoft Jenny',
    'Samantha', // macOS / iOS
    'Daniel',
  ],
}

function localeFor(lang) {
  return LOCALES[lang] ?? LOCALES.de
}

// Velocidade da fala. Ajustável pelo usuário (Configurações) e guardada no
// localStorage — o padrão fica um pouco abaixo do normal por ser texto de estudo.
const RATE_KEY = 'deutsch-app:speech-rate'
const DEFAULT_RATE = 0.85
export const SPEECH_RATE_LIMITS = { min: 0.5, max: 1.1 }

function readStoredRate() {
  try {
    const stored = Number(localStorage.getItem(RATE_KEY))
    if (stored >= SPEECH_RATE_LIMITS.min && stored <= SPEECH_RATE_LIMITS.max) return stored
  } catch {
    /* storage bloqueado */
  }
  return DEFAULT_RATE
}

// Velocidades oferecidas na UI (Configurações e Flashcards), da mais lenta à mais rápida.
export const SPEECH_SPEED_PRESETS = [
  { value: 0.6, label: 'Bem devagar' },
  { value: 0.75, label: 'Devagar' },
  { value: 0.85, label: 'Normal' },
  { value: 1, label: 'Rápido' },
]

let speechRate = speechSupported ? readStoredRate() : DEFAULT_RATE

export function getSpeechRate() {
  return speechRate
}

export function setSpeechRate(value) {
  const { min, max } = SPEECH_RATE_LIMITS
  speechRate = Math.min(max, Math.max(min, value))
  try {
    localStorage.setItem(RATE_KEY, String(speechRate))
  } catch {
    /* storage bloqueado */
  }
}

// Voz resolvida por idioma (a busca é cara, então guardamos o resultado).
const cachedVoice = {}

function scoreVoice(voice, lang) {
  const preferred = PREFERRED_VOICES[lang] ?? []
  const preferredIndex = preferred.findIndex((name) => voice.name?.includes(name))
  let score = preferredIndex === -1 ? 0 : (preferred.length - preferredIndex) * 10
  // No desktop, as vozes remotas (Google) costumam soar bem melhor que as locais.
  if (!voice.localService) score += 3
  const locale = localeFor(lang)
  if (voice.lang === locale) score += 2
  else if (voice.lang?.toLowerCase().startsWith(lang)) score += 1
  return score
}

function resolveVoice(lang) {
  if (cachedVoice[lang]) return cachedVoice[lang]
  const matches = window.speechSynthesis
    .getVoices()
    .filter((voice) => voice.lang?.toLowerCase().startsWith(lang))
  if (matches.length === 0) return null
  cachedVoice[lang] = matches.sort((a, b) => scoreVoice(b, lang) - scoreVoice(a, lang))[0]
  return cachedVoice[lang]
}

if (speechSupported) {
  // A lista de vozes chega de forma assíncrona em alguns navegadores.
  window.speechSynthesis.addEventListener('voiceschanged', () => {
    for (const lang of Object.keys(cachedVoice)) delete cachedVoice[lang]
  })
}

// Resolve quando o navegador já tem a lista de vozes (ou após um tempo limite).
function voicesReady() {
  return new Promise((resolve) => {
    if (window.speechSynthesis.getVoices().length > 0) {
      resolve()
      return
    }
    const done = () => {
      window.speechSynthesis.removeEventListener('voiceschanged', done)
      resolve()
    }
    window.speechSynthesis.addEventListener('voiceschanged', done)
    setTimeout(done, 1000)
  })
}

// Deixa o texto mais "falável": a barra em "Ja / Nein" e as reticências em
// "Hält dieser Zug in...?" são lidas rápido demais; siglas ("IT") soam estranhas.
function normalizeForSpeech(text) {
  return text
    .trim()
    .replace(/\s*\/\s*/g, ', ') // "eins / zwei / drei" -> pausa entre itens
    .replace(/\s*(\.{3,}|…)\s*/g, ', ') // reticências -> pausa clara
    .replace(/\b[A-ZÄÖÜ]{2,}\b/g, (sigla) => sigla.split('').join(' ')) // "IT" -> "I T"
    .replace(/\s{2,}/g, ' ')
    .replace(/\s+([,.?!])/g, '$1')
}

// Quebra em frases para dar um respiro entre elas e evitar o corte do Chrome
// em falas longas (~15s por utterance).
function splitSentences(text) {
  return text
    .split(/(?<=[.?!])\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean)
}

// Chrome pausa a síntese sozinho após ~15s; um resume periódico contorna isso.
let keepAliveTimer = null

function stopKeepAlive() {
  if (keepAliveTimer) {
    clearInterval(keepAliveTimer)
    keepAliveTimer = null
  }
}

function startKeepAlive() {
  stopKeepAlive()
  keepAliveTimer = setInterval(() => {
    if (window.speechSynthesis.speaking) window.speechSynthesis.resume()
    else stopKeepAlive()
  }, 8000)
}

function speakNow(text, lang) {
  const voice = resolveVoice(lang)
  const sentences = splitSentences(normalizeForSpeech(text))

  sentences.forEach((sentence, index) => {
    const utterance = new SpeechSynthesisUtterance(sentence)
    utterance.lang = localeFor(lang)
    utterance.rate = speechRate
    utterance.pitch = 1
    utterance.volume = 1
    if (voice) utterance.voice = voice
    if (index === sentences.length - 1) {
      utterance.onend = stopKeepAlive
      utterance.onerror = stopKeepAlive
    }
    window.speechSynthesis.speak(utterance)
  })

  startKeepAlive()
}

// Fala `text` no idioma `lang` (código ISO 639-1: "de", "en").
export function speak(text, lang = 'de') {
  if (!speechSupported || !text) return
  const synth = window.speechSynthesis
  // Só cancela se algo está tocando — cancel()+speak() imediato tem bug no Chrome
  // e quebra o gesto do usuário no iOS.
  if (synth.speaking || synth.pending) synth.cancel()
  stopKeepAlive()

  if (synth.getVoices().length > 0) speakNow(text, lang)
  else voicesReady().then(() => speakNow(text, lang))
}

export function stopSpeaking() {
  if (!speechSupported) return
  stopKeepAlive()
  window.speechSynthesis.cancel()
}
