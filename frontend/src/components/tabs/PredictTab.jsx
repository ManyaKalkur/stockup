import { useEffect, useState } from 'react'
import { getPrediction } from '../../api'
const LABELS= {
  xgboost: 'XGBoost',
  random_forest: 'Random Forest',
  linear_regression: 'Linear Regression',
  svm: 'SVM',
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
  const maxImpact= Math.max(...data.xgb_explanation.map(f=>Math.abs(f.impact)))

  return (
    <div className="predict-tab">
      <div className="last-close-banner">
        <span className="label">last close</span>
        <span className="mono value big">${data.last_close.toFixed(2)}</span>
      </div>

      <h3>next-close prediction by model</h3>
      <div className="predict-grid">
        {Object.entries(data.predictions).map(([key,val])=>{
          const delta= val-data.last_close
          const pct= (delta/data.last_close)*100
          const up= delta>=0
          return (
            <div key={key} className="predict-card">
              <span className="label">{LABELS[key] || key}</span>
              <span className="mono value" style={{color:up?'var(--up)':'var(--down)'}}>${val.toFixed(2)}</span>
              <span className="mono delta" style={{color:up?'var(--up)':'var(--down)'}}>
                {up?'▲':'▼'} {Math.abs(pct).toFixed(2)}%
              </span>
            </div>
          )
        })}
      </div>

      <h3>What's driving the XGBoost Prediction</h3>
      <p className="explain-note">Positive bars push the price up, negative bars pull it down. Sorted by strength.</p>
      <div className="feature-list">
        {data.xgb_explanation.map(f=>{
          const up= f.impact>=0
          const barWidth= (Math.abs(f.impact)/maxImpact)*100
          return (
            <div key={f.feature} className="feature-row">
              <div className="feature-row-top">
                <span className="mono feature-name">{f.feature}</span>
                <span className="mono" style={{color:up?'var(--up)':'var(--down)'}}>{up?'+':''}{f.impact.toFixed(2)}</span>
              </div>
              <div className="feature-bar-track">
                <div
                  className="feature-bar-fill"
                  style={{width:`${barWidth}%`,background:up?'var(--up)':'var(--down)'}}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}