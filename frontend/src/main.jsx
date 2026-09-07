import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'

import { AuthProvider, useAuth } from './auth/AuthContext.jsx'
import Layout from './components/Layout.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Login from './pages/Login.jsx'
import Review from './pages/Review.jsx'
import Scenarios from './pages/Scenarios.jsx'
import './index.css'

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
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>,
)
