import { useState } from 'react'

export default function Register(){
  const [username,setUsername]=useState('')
  const [password,setPassword]=useState('')

  async function handleRegister(e){
    e.preventDefault()
    const res = await fetch('http://localhost:8000/api/register/', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({username, password})
    })
    const data = await res.json()
    if(data.token){ localStorage.setItem('token', data.token); window.location.reload() }
    else alert(data.error || 'Erro')
  }

  return (
    <form onSubmit={handleRegister}>
      <h2>Registrar</h2>
      <input placeholder='username' value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder='password' value={password} onChange={e=>setPassword(e.target.value)} type='password' />
      <button type='submit'>Registrar</button>
    </form>
  )
}
