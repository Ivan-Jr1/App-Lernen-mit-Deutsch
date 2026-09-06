// Sem autenticação nesta versão: o app inteiro age "como" um dos dois usuários
// fixos, escolhido no cabeçalho e lembrado no localStorage.
import { createContext, useContext, useEffect, useState } from 'react'

const USERS = [
  { username: 'ivan', label: 'Ivan' },
  { username: 'esposa', label: 'Esposa' },
]
const STORAGE_KEY = 'deutsch-app:user'

const UserContext = createContext(null)

export function UserProvider({ children }) {
  const [username, setUsername] = useState(() => {
    return localStorage.getItem(STORAGE_KEY) || USERS[0].username
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, username)
  }, [username])

  return (
    <UserContext.Provider value={{ username, setUsername, users: USERS }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (!context) throw new Error('useUser precisa estar dentro de <UserProvider>')
  return context
}
