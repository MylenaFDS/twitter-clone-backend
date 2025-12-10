import { useState } from 'react'
import Login from './components/Login'
import Feed from './components/Feed'

export default function App(){
  const [token, setToken] = useState(localStorage.getItem('token'))
  return token ? <Feed token={token} setToken={setToken} /> : <Login setToken={setToken} />
}
