// Alterna o modo claro/escuro adicionando a classe .dark no <html> e guarda a
// preferência. O valor inicial já foi aplicado por um script inline no index.html
// para evitar flash.

import { useCallback, useEffect, useState } from 'react'

const STORAGE_KEY = 'deutsch-app:theme'

export function useTheme() {
  const [isDark, setIsDark] = useState(() =>
    document.documentElement.classList.contains('dark'),
  )

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark)
    try {
      localStorage.setItem(STORAGE_KEY, isDark ? 'dark' : 'light')
    } catch {
      /* storage bloqueado — segue só na sessão */
    }
  }, [isDark])

  const toggle = useCallback(() => setIsDark((value) => !value), [])
  return { isDark, toggle }
}
