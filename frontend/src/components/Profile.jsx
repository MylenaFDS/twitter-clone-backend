import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Profile({ token }){
  const [profile, setProfile] = useState(null)

  useEffect(()=>{
    (async ()=>{
      const data = await api('/profile/', 'GET', null, token)
      setProfile(data)
    })()
  },[])

  if(!profile) return <div>Carregando...</div>
  return (
    <div>
      <h2>{profile.user.username}</h2>
      <img src={profile.avatar || ''} alt='' style={{width:80,height:80}}/>
      <p>{profile.bio}</p>
    </div>
  )
}
