import { lazy, StrictMode, Suspense } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'

import { AuthProvider, useAuth } from './auth/AuthContext.jsx'
import { api } from './lib/api.js'
import Layout from './components/Layout.jsx'
import { Spinner } from './components/ui.jsx'
import './index.css'

// Cada página vira um chunk separado: a tela de Login não baixa mais o código
// de Dashboard/Review/Scenarios/Settings junto.
const Dashboard = lazy(() => import('./pages/Dashboard.jsx'))
const Login = lazy(() => import('./pages/Login.jsx'))
const Review = lazy(() => import('./pages/Review.jsx'))
const Scenarios = lazy(() => import('./pages/Scenarios.jsx'))
const Settings = lazy(() => import('./pages/Settings.jsx'))

// Acorda a API do Render (free tier hiberna após 15 min) já no carregamento,
// em paralelo com o resto — encurta a espera da primeira tela.
api.health().catch(() => {})

function RequireAuth() {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? <Layout /> : <Navigate to="/login" replace />
}

function LoginRoute() {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? <Navigate to="/review" replace /> : <Login />
}

const router = createBrowserRouter([
  { path: '/login', element: <LoginRoute /> },
  {
    path: '/',
    element: <RequireAuth />,
    children: [
      { index: true, element: <Navigate to="/review" replace /> },
      { path: 'review', element: <Review /> },
      { path: 'scenarios', element: <Scenarios /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <Suspense
        fallback={
          <div className="grid min-h-screen place-items-center">
            <Spinner />
          </div>
        }
      >
        <RouterProvider router={router} />
      </Suspense>
    </AuthProvider>
  </StrictMode>,
)
