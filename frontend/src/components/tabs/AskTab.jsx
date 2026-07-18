import { useState } from 'react'
import { ingest, askQuestion } from '../../api'

export default function AskTab({symbol}) {
  const [question,setQuestion]= useState('')
  const [answer,setAnswer]= useState(null)
  const [loading,setLoading]= useState(false)
  const [indexing,setIndexing]= useState(false)

  async function handleIndex() {
    setIndexing(true)
    await ingest(symbol).catch(()=>{})
    setIndexing(false)
  }

  async function handleAsk(e) {
    e.preventDefault()
    if (!question.trim()) return
    setLoading(true)
    const result= await askQuestion(symbol,question).catch(()=>({answer:'something went wrong, try again',sources:[]}))
    setAnswer(result)
    setLoading(false)
  }

  if (!symbol) return <div className="empty-state">search a ticker to ask about it</div>

  return (
    <div className="ask-tab">
      <div className="ask-index-row">
        <span className="label">indexed news + filings power this; refresh if answers feel stale</span>
        <button onClick={handleIndex} disabled={indexing}>{indexing?'indexing...':'index latest data'}</button>
      </div>

      <form onSubmit={handleAsk} className="ask-form">
        <input
          placeholder={`why did ${symbol} move today?`}
          value={question}
          onChange={e=>setQuestion(e.target.value)}
        />
        <button type="submit" disabled={loading}>{loading?'thinking...':'ask'}</button>
      </form>

      {answer && (
        <div className="answer-block">
          <p>{answer.answer}</p>
          {answer.sources?.length>0 && (
            <div className="sources">
              {answer.sources.map((s,i)=>(
                <a key={i} href={s.url} target="_blank" rel="noreferrer" className="source-chip mono">
                  {s.source} · {s.date?.slice(0,10)}
                </a>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}