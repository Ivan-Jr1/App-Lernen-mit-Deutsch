// Peças de UI reaproveitadas. Mantidas pequenas e sem estado.

import { useEffect, useState } from 'react'

import { apiHasResponded } from '../lib/api.js'

const BUTTON_VARIANTS = {
  primary:
    'bg-indigo-600 text-white hover:bg-indigo-500 active:bg-indigo-700 disabled:bg-indigo-600/50',
  secondary:
    'bg-zinc-100 text-zinc-800 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-100 dark:hover:bg-zinc-700',
  ghost:
    'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-zinc-800 dark:hover:text-zinc-100',
}

export function Button({ variant = 'primary', className = '', ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold
        transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500
        disabled:cursor-not-allowed ${BUTTON_VARIANTS[variant]} ${className}`}
      {...props}
    />
  )
}

export function Card({ className = '', ...props }) {
  return (
    <div
      className={`rounded-2xl border border-zinc-200 bg-white shadow-sm
        dark:border-zinc-800 dark:bg-zinc-900 ${className}`}
      {...props}
    />
  )
}

export function Spinner({ label }) {
  // Se a espera passar de alguns segundos e a API ainda não respondeu nesta
  // sessão, provavelmente o servidor gratuito está acordando — avisa o usuário.
  const [waking, setWaking] = useState(false)
  useEffect(() => {
    const timer = setTimeout(() => setWaking(true), 4000)
    return () => clearTimeout(timer)
  }, [])

  const message =
    waking && !apiHasResponded()
      ? 'O servidor gratuito estava dormindo — acordando, leva ~30 s na primeira vez…'
      : label

  return (
    <div className="mx-auto flex max-w-xs flex-col items-center gap-3 py-16 text-center text-sm text-zinc-400">
      <span className="size-6 animate-spin rounded-full border-2 border-zinc-300 border-t-indigo-500 dark:border-zinc-700 dark:border-t-indigo-400" />
      {message}
    </div>
  )
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="animate-rise rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/40 dark:text-red-300">
      <p className="font-medium">Algo deu errado</p>
      <p className="mt-1 opacity-90">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 font-semibold underline underline-offset-4 hover:opacity-80"
        >
          Tentar de novo
        </button>
      )}
    </div>
  )
}

export function EmptyState({ icon = '✨', title, children }) {
  return (
    <div className="animate-rise flex flex-col items-center rounded-2xl border border-dashed border-zinc-300 bg-white/50 px-6 py-14 text-center dark:border-zinc-700 dark:bg-zinc-900/40">
      <span className="text-3xl">{icon}</span>
      <p className="mt-3 text-lg font-semibold text-zinc-800 dark:text-zinc-100">{title}</p>
      {children && <div className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">{children}</div>}
    </div>
  )
}

export function Avatar({ src, name, className = 'size-9' }) {
  if (src) {
    return (
      <img
        src={src}
        alt={name ?? ''}
        className={`shrink-0 rounded-full object-cover ${className}`}
      />
    )
  }
  return (
    <span
      className={`grid shrink-0 place-items-center rounded-full bg-zinc-200 font-bold text-zinc-600 dark:bg-zinc-700 dark:text-zinc-200 ${className}`}
    >
      {name?.[0]?.toUpperCase() ?? '?'}
    </span>
  )
}

export function Badge({ tone = 'zinc', children }) {
  const tones = {
    zinc: 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300',
    amber: 'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300',
    indigo: 'bg-indigo-100 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300',
  }
  return (
    <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${tones[tone]}`}>{children}</span>
  )
}
