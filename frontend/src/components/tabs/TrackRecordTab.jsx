import { useEffect, useState } from 'react'
import { getAccuracy } from '../../api'

const LABELS= {
  xgboost: 'XGBoost',
  random_forest: 'Random Forest',
  linear_regression: 'Linear Regression',
  svm: 'SVM',
}

export default function TrackRecordTab({symbol}) {
  const [data,setData]= useState(null)
  const [loading,setLoading]= useState(false)
  const [error,setError]= useState(null)
  useEffect(()=>{
    if (!symbol) return
    setLoading(true); setError(null); setData(null)
    getAccuracy(symbol)
      .then(setData)
      .catch(()=>setError('no prediction history yet for this ticker'))
      .finally(()=>setLoading(false))
  },[symbol])

  if (!symbol) return <div className="empty-state">Search a ticker to see its prediction track record</div>
  if (loading) return <div className="empty-state">Loading track record...</div>
  if (error) return <div className="empty-state">{error}</div>
  if (!data) return null

  const models= Object.entries(data.summary)
  if (models.length===0) {
    return (
      <div className="empty-state">
        No resolved predictions yet. Predictions get checked against real prices the day after they're made, come back tomorrow to start seeing accuracy.
      </div>
    )
  }

  return (
    <div className="track-record-tab">
      <h3>Average error by model</h3>
      <p className="explain-note">Lower is better. This compares each model's predicted next-day price against what actually happened.</p>
      <div className="predict-grid">
        {models.map(([key,stats])=>(
          <div key={key} className="predict-card">
            <span className="label">{LABELS[key] || key}</span>
            <span className="mono value">{stats.avg_error_pct}%</span>
            <span className="mono delta">{stats.count} resolved prediction{stats.count!==1?'s':''}</span>
          </div>
        ))}
      </div>

      <h3>Recent predictions vs Actual</h3>
      <div className="feature-list">
        {data.recent.map((r,i)=>{
          const diff= r.actual - r.predicted
          const pct= (diff/r.actual)*100
          return (
            <div key={i} className="feature-row">
              <div className="feature-row-top">
                <span className="mono feature-name">{LABELS[r.model] || r.model} · {r.target_date.slice(0,10)}</span>
                <span className="mono" style={{color:Math.abs(pct)<2?'var(--up)':'var(--down)'}}>
                  {pct>=0?'+':''}{pct.toFixed(2)}% off
                </span>
              </div>
              <div className="track-record-numbers mono">
                Predicted ${r.predicted.toFixed(2)} : Actual ${r.actual.toFixed(2)}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}