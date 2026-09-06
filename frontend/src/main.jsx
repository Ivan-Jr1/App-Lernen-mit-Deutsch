import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'

import App from './App.jsx'
import './index.css'
import Dashboard from './pages/Dashboard.jsx'
import Review from './pages/Review.jsx'
import Scenarios from './pages/Scenarios.jsx'
import { UserProvider } from './user.jsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Navigate to="/review" replace /> },
      { path: 'review', element: <Review /> },
      { path: 'scenarios', element: <Scenarios /> },
      { path: 'dashboard', element: <Dashboard /> },
    ],
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <UserProvider>
      <RouterProvider router={router} />
    </UserProvider>
  </StrictMode>,
)
