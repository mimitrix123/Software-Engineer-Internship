import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [email, setEmail] = useState('demo@example.com');
  const [password, setPassword] = useState('password123');
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [live, setLive] = useState('Connecting…');

  async function auth(path) {
    const r = await fetch(`${API}${path}`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({email,password})});
    const data = await r.json();
    if (!r.ok) return alert(data.detail || 'Authentication failed');
    localStorage.setItem('token', data.access_token); setToken(data.access_token);
  }
  async function load() {
    if (!token) return;
    const r = await fetch(`${API}/projects`, {headers:{Authorization:`Bearer ${token}`}});
    if (r.ok) setProjects(await r.json());
  }
  async function create() {
    const r = await fetch(`${API}/projects`, {method:'POST', headers:{'Content-Type':'application/json',Authorization:`Bearer ${token}`}, body:JSON.stringify({name,description})});
    if (r.ok) { setName(''); setDescription(''); load(); }
  }
  useEffect(() => { load(); }, [token]);
  useEffect(() => { const ws = new WebSocket(API.replace('http','ws') + '/ws'); ws.onopen=()=>setLive('Live'); ws.onclose=()=>setLive('Offline'); return ()=>ws.close(); }, []);
  return <main><header><h1>Acme SaaS</h1><span>Realtime: {live}</span></header>
    {!token ? <section className="card"><h2>Sign in</h2><input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/><input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password"/><button onClick={()=>auth('/auth/login')}>Login</button><button onClick={()=>auth('/auth/register')}>Create account</button></section> : <>
    <section className="card"><h2>Create project</h2><input value={name} onChange={e=>setName(e.target.value)} placeholder="Project name"/><textarea value={description} onChange={e=>setDescription(e.target.value)} placeholder="Description"/><button onClick={create}>Create</button></section>
    <section><h2>Your projects</h2>{projects.map(p=><article className="card" key={p.id}><h3>{p.name}</h3><p>{p.description}</p></article>)}</section></>}
  </main>
}
createRoot(document.getElementById('root')).render(<App />);
