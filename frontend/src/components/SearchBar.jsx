import { useState } from 'react'

export default function SearchBar({onSelect}) {
  const [value,setValue]= useState('')
  const [error,setError]= useState(null)

  function submit(e) {
    e.preventDefault()
    if (!value.trim()) return
    setError(null)
    onSelect(value.trim().toUpperCase())
  }

  return (
    <form className="search-bar" onSubmit={submit}>
      <input
        className="mono"
        placeholder="search a ticker : AAPL, TSLA, NVDA..."
        value={value}
        onChange={e=>setValue(e.target.value)}
      />
      <button type="submit" className="search-btn">go</button>
      {error && <span className="search-error">{error}</span>}
    </form>
  )
}