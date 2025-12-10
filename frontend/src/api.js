const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export async function api(path, method='GET', body=null, token=null){
  const headers = {'Content-Type':'application/json'}
  if(token) headers['Authorization'] = `Token ${token}`
  const res = await fetch(`${API_BASE}${path}`, {
    method, headers, body: body ? JSON.stringify(body) : null
  })
  if(res.status === 204) return null
  return res.json()
}
