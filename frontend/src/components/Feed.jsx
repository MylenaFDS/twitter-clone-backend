import { useEffect, useState } from 'react'
import { api } from '../api'

export default function Feed({ token, setToken }){
  const [posts, setPosts] = useState([])
  const [content, setContent] = useState('')

  useEffect(()=>{ fetchPosts() }, [])

  async function fetchPosts(){
    const data = await api('/feed/', 'GET', null, token)
    setPosts(data || [])
  }

  async function createPost(e){
    e.preventDefault()
    await api('/posts/', 'POST', {content}, token)
    setContent('')
    fetchPosts()
  }

  function logout(){
    localStorage.removeItem('token'); setToken(null)
  }

  return (
    <div>
      <button onClick={logout}>Logout</button>
      <h1>Feed</h1>
      <form onSubmit={createPost}>
        <textarea value={content} onChange={e=>setContent(e.target.value)} placeholder='O que está acontecendo?'></textarea>
        <button type='submit'>Publicar</button>
      </form>
      {posts.map(p=>(
        <div key={p.id} style={{border:'1px solid #ddd', padding:8, margin:8}}>
          <strong>{p.author.username}</strong> <small>{new Date(p.created_at).toLocaleString()}</small>
          <p>{p.content}</p>
          <div>Likes: {p.likes_count} • Comments: {p.comments_count}</div>
        </div>
      ))}
    </div>
  )
}
