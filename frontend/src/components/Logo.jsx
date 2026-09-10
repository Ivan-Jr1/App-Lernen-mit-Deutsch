// Marca do app: um flashcard virando (deck de cartões). Usa a cor de destaque
// (--color-accent-*), que segue o idioma estudado.

export function LogoMark({ className = 'size-8' }) {
  return (
    <span
      className={`inline-block overflow-hidden rounded-lg ${className}`}
      aria-hidden="true"
    >
      <svg viewBox="0 0 24 24" className="size-full">
        <rect width="24" height="24" fill="var(--color-accent-600)" />
        {/* carta de trás, levemente girada — dá a ideia de virar o cartão */}
        <rect
          x="7"
          y="4.5"
          width="12"
          height="15"
          rx="2.4"
          fill="var(--color-accent-200)"
          transform="rotate(9 13 12)"
        />
        {/* carta da frente */}
        <rect x="4.6" y="5" width="12" height="15" rx="2.4" fill="#ffffff" />
        {/* linhas de "texto" na carta da frente */}
        <rect x="7" y="9" width="7.2" height="1.7" rx="0.85" fill="var(--color-accent-200)" />
        <rect x="7" y="12.4" width="4.8" height="1.7" rx="0.85" fill="var(--color-accent-200)" />
      </svg>
    </span>
  )
}

export function Logo({ markClass }) {
  return (
    <div className="flex items-center gap-2">
      <LogoMark className={markClass} />
      <span className="text-[15px] font-bold tracking-tight">Learning Languages</span>
    </div>
  )
}
