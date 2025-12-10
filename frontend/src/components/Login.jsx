import { useState } from 'react'
import { api } from '../api'

export default function Login({ setToken }){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  async function handleLogin(e){
    e.preventDefault()
    const res = await fetch('http://localhost:8000/api/login/', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({username, password})
    })
    const data = await res.json()
    if(data.token){
      localStorage.setItem('token', data.token)
      setToken(data.token)
    } else {
      alert(data.error || 'Erro')
    }
  }

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>
      <input placeholder='username' value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder='password' value={password} onChange={e=>setPassword(e.target.value)} type='password' />
      <button type='submit'>Entrar</button>
    </form>
  )
}
