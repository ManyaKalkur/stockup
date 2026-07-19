const BASE= import.meta.env.VITE_API_BASE || '/api'

export async function pingHealth() {
  const healthUrl= BASE.replace(/\/api$/,'')+'/health'
  const res= await fetch(healthUrl)
  if (!res.ok) throw new Error('not ready')
  return res.json()
}

export async function searchTicker(symbol) {
  const res= await fetch(`${BASE}/data/search/${symbol}`)
  if (!res.ok) throw new Error('not found')
  return res.json()
}

export async function getPrices(symbol, period='6mo') {
  const res= await fetch(`${BASE}/data/prices/${symbol}?period=${period}`)
  if (!res.ok) throw new Error('failed to load prices')
  return res.json()
}

export async function getPrediction(symbol) {
  const res= await fetch(`${BASE}/ml/predict/${symbol}`)
  if (!res.ok) throw new Error('failed to predict')
  return res.json()
}

export async function ingest(symbol) {
  const res= await fetch(`${BASE}/rag/ingest/${symbol}`, { method:'POST'})
  if (!res.ok) throw new Error('failed to ingest')
  return res.json()
}

export async function askQuestion(symbol, question) {
  const res= await fetch(`${BASE}/rag/ask/${symbol}?question=${encodeURIComponent(question)}`)
  if (!res.ok) throw new Error('failed to get answer')
  return res.json()
}

export async function getReport(symbol) {
  const res= await fetch(`${BASE}/agent/report/${symbol}`)
  if (!res.ok) throw new Error('failed to generate report')
  return res.json()
}

export function liveSocket(symbol) {
  const apiBase= import.meta.env.VITE_API_BASE || `${window.location.protocol}//${window.location.host}/api`
  const wsBase= apiBase.replace(/^http/,'ws')
  return new WebSocket(`${wsBase}/data/ws/${symbol}`)
}