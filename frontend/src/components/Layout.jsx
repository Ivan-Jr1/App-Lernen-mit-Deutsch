// Casca do app: sidebar no desktop, barra inferior no celular.

import { Suspense } from 'react'
import { NavLink, Outlet } from 'react-router-dom'

import { useAuth } from '../auth/AuthContext.jsx'
import { useTheme } from '../lib/theme.js'
import {
  CardsIcon,
  ChartIcon,
  ChatIcon,
  LogoutIcon,
  MoonIcon,
  SettingsIcon,
  SunIcon,
} from './icons.jsx'
import { Logo } from './Logo.jsx'
import { Avatar, Badge, Spinner } from './ui.jsx'

const NAV = [
  { to: '/review', label: 'Flashcards', Icon: CardsIcon },
  { to: '/scenarios', label: 'Cenários', Icon: ChatIcon },
  { to: '/dashboard', label: 'Dashboard', Icon: ChartIcon },
]

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

function ProfileLink({ compact = false }) {
  const { user, isGuest } = useAuth()
  return (
    <NavLink
      to="/settings"
      className={({ isActive }) =>
        `flex items-center gap-2.5 rounded-lg ${compact ? '' : 'p-1'} ${
          isActive && !compact ? 'bg-zinc-100 dark:bg-zinc-800' : ''
        }`
      }
    >
      <Avatar src={user?.avatar_url} name={user?.display_name} className="size-9" />
      {!compact && (
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold">{user?.display_name}</p>
          {isGuest ? (
            <Badge tone="amber">somente leitura</Badge>
          ) : (
            <p className="text-xs text-zinc-400">ver perfil</p>
          )}
        </div>
      )}
    </NavLink>
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
              ? 'text-accent-600 dark:text-accent-400'
              : 'bg-accent-50 text-accent-700 dark:bg-accent-950/50 dark:text-accent-300'
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
  const { logout } = useAuth()

  return (
    <div className="mx-auto flex min-h-screen w-full max-w-6xl">
      {/* faixa de destaque no topo — cores da bandeira do idioma ativo */}
      <div className="brand-stripe fixed inset-x-0 top-0 z-20 h-1" />

      {/* Sidebar — desktop */}
      <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col border-r border-zinc-200 p-4 pt-5 md:flex dark:border-zinc-800">
        <Logo />
        <nav className="mt-8 flex flex-1 flex-col gap-1">
          {NAV.map((item) => (
            <NavItem key={item.to} {...item} />
          ))}
          <NavItem to="/settings" label="Configurações" Icon={SettingsIcon} />
        </nav>
        <div className="space-y-2 border-t border-zinc-200 pt-4 dark:border-zinc-800">
          <div className="flex items-center justify-between">
            <ProfileLink />
            <ThemeToggle />
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 px-1 text-sm text-zinc-500 transition-colors hover:text-zinc-800 dark:hover:text-zinc-100"
          >
            <LogoutIcon className="size-4" /> Sair
          </button>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Topbar — celular */}
        <header className="sticky top-0 z-10 flex items-center justify-between border-b border-zinc-200 bg-zinc-50/90 px-4 py-3 pt-4 backdrop-blur md:hidden dark:border-zinc-800 dark:bg-zinc-950/90">
          <Logo />
          <div className="flex items-center gap-1">
            <ThemeToggle />
            <ProfileLink compact />
          </div>
        </header>

        <main className="flex-1 px-4 py-6 pb-24 md:px-10 md:py-10 md:pb-10">
          <div className="mx-auto max-w-2xl">
            <Suspense fallback={<Spinner />}>
              <Outlet />
            </Suspense>
          </div>
        </main>

        {/* Barra inferior — celular */}
        <nav className="fixed inset-x-0 bottom-0 z-10 flex border-t border-zinc-200 bg-white/95 backdrop-blur md:hidden dark:border-zinc-800 dark:bg-zinc-900/95">
          {NAV.map((item) => (
            <NavItem key={item.to} {...item} variant="mobile" />
          ))}
          <NavItem to="/settings" label="Perfil" Icon={SettingsIcon} variant="mobile" />
        </nav>
      </div>
    </div>
  )
}
