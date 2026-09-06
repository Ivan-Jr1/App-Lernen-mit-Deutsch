import { NavLink, Outlet } from 'react-router-dom'

import { useUser } from './user.jsx'

const NAV_ITEMS = [
  { to: '/review', label: 'Flashcards' },
  { to: '/scenarios', label: 'Cenários' },
  { to: '/dashboard', label: 'Dashboard' },
]

function UserSwitcher() {
  const { username, setUsername, users } = useUser()
  return (
    <div className="flex gap-1 rounded-lg bg-slate-100 p-1">
      {users.map((user) => (
        <button
          key={user.username}
          onClick={() => setUsername(user.username)}
          className={`rounded-md px-3 py-1 text-sm font-medium transition ${
            username === user.username
              ? 'bg-white text-slate-900 shadow-sm'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          {user.label}
        </button>
      ))}
    </div>
  )
}

export default function App() {
  return (
    <div className="mx-auto min-h-screen max-w-2xl px-4 pb-16">
      <header className="flex items-center justify-between py-6">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🇩🇪</span>
          <span className="text-lg font-bold tracking-tight">Deutsch App</span>
        </div>
        <UserSwitcher />
      </header>

      <nav className="mb-8 flex gap-1 border-b border-slate-200">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `-mb-px border-b-2 px-4 py-2 text-sm font-medium transition ${
                isActive
                  ? 'border-slate-900 text-slate-900'
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <main>
        <Outlet />
      </main>
    </div>
  )
}
