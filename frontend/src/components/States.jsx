// Estados de carregamento / erro / vazio reaproveitados pelas três telas.

export function Loading({ label = 'Carregando…' }) {
  return <p className="py-12 text-center text-sm text-slate-400">{label}</p>
}

export function ErrorBox({ message, onRetry }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
      <p>{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 font-medium text-red-800 underline underline-offset-2"
        >
          Tentar de novo
        </button>
      )}
    </div>
  )
}

export function EmptyState({ children }) {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 bg-white py-12 text-center text-slate-500">
      {children}
    </div>
  )
}
