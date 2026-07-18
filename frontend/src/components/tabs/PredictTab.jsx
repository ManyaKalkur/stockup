import { useEffect, useState } from 'react'
import { getPrediction } from '../../api'

export default function PredictTab({symbol}) {
  const [data,setData]= useState(null)
  const [loading,setLoading]= useState(false)
  const [error,setError]= useState(null)

  useEffect(()=>{
    if (!symbol) return
    setLoading(true); setError(null); setData(null)
    getPrediction(symbol)
  .then(setData)
  .catch(async (err)=> {
    console.error(err);
    setError(err.response?.data?.detail || err.message);
  });
  },[symbol])

  if (!symbol) return <div className="empty-state">search a ticker to run predictions</div>
  if (loading) return <div className="empty-state">training models on {symbol}...</div>
  if (error) return <div className="empty-state">{error}</div>
  if (!data) return null

  const xgbDelta= data.xgb_prediction-data.last_close
  const lstmDelta= data.lstm_prediction-data.last_close

  return (
    <div className="predict-tab">
      <div className="predict-grid">
        <div className="predict-card">
          <span className="label">last close</span>
          <span className="mono value">${data.last_close.toFixed(2)}</span>
        </div>
        <div className="predict-card">
          <span className="label">xgboost predicts</span>
          <span className="mono value" style={{color:xgbDelta>=0?'var(--up)':'var(--down)'}}>${data.xgb_prediction.toFixed(2)}</span>
        </div>
        <div className="predict-card">
          <span className="label">lstm predicts</span>
          <span className="mono value" style={{color:lstmDelta>=0?'var(--up)':'var(--down)'}}>${data.lstm_prediction.toFixed(2)}</span>
        </div>
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