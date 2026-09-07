// Marca do app: quadradinho com as faixas da bandeira alemã (preto/vermelho/dourado).

export function LogoMark({ className = 'size-8' }) {
  return (
    <span
      className={`inline-block overflow-hidden rounded-lg ring-1 ring-black/10 ${className}`}
      aria-hidden="true"
    >
      <svg viewBox="0 0 24 24" className="size-full">
        <rect width="24" height="8" y="0" fill="#000000" />
        <rect width="24" height="8" y="8" fill="#DD0000" />
        <rect width="24" height="8" y="16" fill="#FFCE00" />
      </svg>
    </span>
  )
}

export function Logo({ markClass }) {
  return (
    <div className="flex items-center gap-2">
      <LogoMark className={markClass} />
      <span className="text-[15px] font-bold tracking-tight">Deutsch App</span>
    </div>
  )
}
