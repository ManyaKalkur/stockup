import { useEffect, useState } from 'react'
import { getReport } from '../../api'
const LABELS = {
  xgboost: 'xgboost',
  random_forest: 'random forest',
  linear_regression: 'linear regression',
  svm: 'svm',
}

export default function ReportTab({symbol}) {
  const [data,setData]= useState(null)
  const [loading,setLoading]= useState(false)
  const [error,setError]= useState(null)

  useEffect(()=>{
    if (!symbol) return
    setLoading(true); setError(null); setData(null)
    getReport(symbol)
      .then(setData)
      .catch(()=>setError('couldn\'t generate a report. Try indexing news for this ticker first'))
      .finally(()=>setLoading(false))
  },[symbol])

  if (!symbol) return <div className="empty-state">search a ticker for a synthesized report</div>
  if (loading) return <div className="empty-state">pulling price data, running models, reading recent news...</div>
  if (error) return <div className="empty-state">{error}</div>
  if (!data) return null
  const values= Object.values(data.predictions)
  const disagree= values.some(v=>Math.sign(v-data.last_close) !== Math.sign(values[0]-data.last_close))

  return (
    <div className="report-tab">
      <div className="report-summary">{data.summary}</div>
      {disagree && <div className="report-flag">models disagree on direction; Treat this one with extra caution</div>}
      <div className="predict-grid">
        <div className="predict-card">
          <span className="label">last close</span>
          <span className="mono value">${data.last_close.toFixed(2)}</span>
        </div>
        {Object.entries(data.predictions).map(([key,val])=>(
          <div key={key} className="predict-card">
            <span className="label">{LABELS[key] || key}</span>
            <span className="mono value">${val.toFixed(2)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}