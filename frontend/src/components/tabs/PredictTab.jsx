import { useEffect, useState } from 'react'
import { getPrediction } from '../../api'
const LABELS= {
  xgboost: 'xgboost',
  random_forest: 'random forest',
  linear_regression: 'linear regression',
  svm: 'svm',
}

export default function PredictTab({symbol}) {
  const [data,setData]= useState(null)
  const [loading,setLoading]= useState(false)
  const [error,setError]= useState(null)

  useEffect(()=>{
    if (!symbol) return
    setLoading(true); setError(null); setData(null)
    getPrediction(symbol)
      .then(setData)
      .catch(()=>setError('not enough history to train on this ticker'))
      .finally(()=>setLoading(false))
  },[symbol])

  if (!symbol) return <div className="empty-state">search a ticker to run predictions</div>
  if (loading) return <div className="empty-state">training models on {symbol}...</div>
  if (error) return <div className="empty-state">{error}</div>
  if (!data) return null

  return (
    <div className="predict-tab">
      <div className="predict-grid">
        <div className="predict-card">
          <span className="label">last close</span>
          <span className="mono value">${data.last_close.toFixed(2)}</span>
        </div>
        {Object.entries(data.predictions).map(([key,val])=>{
          const delta= val-data.last_close
          return (
            <div key={key} className="predict-card">
              <span className="label">{LABELS[key] || key}</span>
              <span className="mono value" style={{color:delta>=0?'var(--up)':'var(--down)'}}>${val.toFixed(2)}</span>
            </div>
          )
        })}
      </div>

      <h3>what's driving the xgboost prediction</h3>
      <div className="feature-list">
        {data.xgb_explanation.map(f=>(
          <div key={f.feature} className="feature-row">
            <span className="mono">{f.feature}</span>
            <span className="mono" style={{color:f.impact>=0?'var(--up)':'var(--down)'}}>{f.impact>=0?'+':''}{f.impact}</span>
          </div>
        ))}
      </div>
    </div>
  )
}