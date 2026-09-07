// Casca do app: sidebar no desktop, barra inferior no celular.

import { NavLink, Outlet } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext.jsx'
import { useTheme } from '../lib/theme.js'
import { CardsIcon, ChartIcon, ChatIcon, LogoutIcon, MoonIcon, SunIcon } from './icons.jsx'
import { Badge } from './ui.jsx'

const NAV = [
  { to: '/review', label: 'Flashcards', Icon: CardsIcon },
  { to: '/scenarios', label: 'Cenários', Icon: ChatIcon },
  { to: '/dashboard', label: 'Dashboard', Icon: ChartIcon },
]

function Logo() {
  return (
    <div className="flex items-center gap-2">
      <span className="grid size-8 place-items-center rounded-lg bg-indigo-600 text-sm font-black text-white">
        DE
      </span>
      <span className="text-[15px] font-bold tracking-tight">Deutsch App</span>
    </div>
  )
}

function ThemeToggle() {
  const { isDark, toggle } = useTheme()
  return (
    <button
      onClick={toggle}
      aria-label={isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
      className="grid size-9 place-items-center rounded-lg text-zinc-500 transition-colors hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-zinc-800 dark:hover:text-zinc-100"
    >
      {isDark ? <SunIcon className="size-5" /> : <MoonIcon className="size-5" />}
    </button>
  )
}

function UserBlock({ compact = false }) {
  const { user, isGuest, logout } = useAuth()
  return (
    <div className={compact ? 'flex items-center gap-2' : 'space-y-3'}>
      <div className="flex items-center gap-2.5">
        <span className="grid size-9 shrink-0 place-items-center rounded-full bg-zinc-200 text-sm font-bold text-zinc-600 dark:bg-zinc-700 dark:text-zinc-200">
          {user?.display_name?.[0] ?? '?'}
        </span>
        {!compact && (
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold">{user?.display_name}</p>
            {isGuest && <Badge tone="amber">somente leitura</Badge>}
          </div>
        )}
      </div>
      <button
        onClick={logout}
        className="flex items-center gap-2 rounded-lg text-sm text-zinc-500 transition-colors hover:text-zinc-800 dark:hover:text-zinc-100"
      >
        <LogoutIcon className="size-4" /> {compact ? '' : 'Sair'}
      </button>
    </div>
  )
}

function NavItem({ to, label, Icon, variant = 'desktop' }) {
  const isMobile = variant === 'mobile'
  const shape = isMobile
    ? 'flex flex-1 flex-col items-center gap-1 py-2 text-[11px] font-medium'
    : 'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium'
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        [
          shape,
          'transition-colors',
          isActive
            ? isMobile
              ? 'text-indigo-600 dark:text-indigo-400'
              : 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-300'
            : 'text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100',
        ].join(' ')
      }
    >
      <Icon className={isMobile ? 'size-5' : 'size-[18px]'} />
      {label}
    </NavLink>
  )
}

export default function Layout() {
  return (
    <div className="mx-auto flex min-h-screen w-full max-w-6xl">
      {/* Sidebar — desktop */}
      <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col border-r border-zinc-200 p-4 md:flex dark:border-zinc-800">
        <Logo />
        <nav className="mt-8 flex flex-1 flex-col gap-1">
          {NAV.map((item) => (
            <NavItem key={item.to} {...item} />
          ))}
        </nav>
        <div className="flex items-center justify-between border-t border-zinc-200 pt-4 dark:border-zinc-800">
          <UserBlock />
          <ThemeToggle />
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Topbar — celular */}
        <header className="sticky top-0 z-10 flex items-center justify-between border-b border-zinc-200 bg-zinc-50/90 px-4 py-3 backdrop-blur md:hidden dark:border-zinc-800 dark:bg-zinc-950/90">
          <Logo />
          <div className="flex items-center gap-1">
            <ThemeToggle />
            <UserBlock compact />
          </div>
        </header>

        <main className="flex-1 px-4 py-6 pb-24 md:px-10 md:py-10 md:pb-10">
          <div className="mx-auto max-w-2xl">
            <Outlet />
          </div>
        </main>

        {/* Barra inferior — celular */}
        <nav className="fixed inset-x-0 bottom-0 z-10 flex border-t border-zinc-200 bg-white/95 backdrop-blur md:hidden dark:border-zinc-800 dark:bg-zinc-900/95">
          {NAV.map((item) => (
            <NavItem key={item.to} {...item} variant="mobile" />
          ))}
        </nav>
      </div>
    </div>
  )
}
