import { useEffect, useState } from 'react'
import { getPrediction } from '../../api'
const LABELS= {
  xgboost: 'XGBoost',
  random_forest: 'Random Forest',
  linear_regression: 'Linear Regression',
  svm: 'SVM',
}
const FEATURE_NAMES = {
  sma_10: '10-Day Simple Moving Average',
  sma_30: '30-Day Simple Moving Average',
  ema_10: '10-Day Exponential Moving Average',
  rsi_14: '14-Day Relative Strength Index',
  macd: 'MACD',
  macd_signal: 'MACD Signal Line',
  volatility_10: '10-Day Volatility',
  return_1d: '1-Day Return',
  volume: 'Trading Volume',
}
const FEATURE_INFO = {
  sma_10: '10-day average price. Smooths short-term noise, price sitting above it usually signals upward momentum.',
  sma_30: '30-day average price. A slower trend line, crossing above or below it often marks a bigger trend shift.',
  ema_10: '10-day exponential average. Weights recent prices more, so it reacts faster than a simple average.',
  rsi_14: '14-day Relative Strength Index (0-100). Above 70 suggests overbought, below 30 suggests oversold.',
  macd: 'Gap between a fast and slow moving average. Shows the direction and strength of momentum.',
  macd_signal: 'Smoothed average of the MACD line. Crossovers between the two often flag momentum shifts.',
  volatility_10: '10-day price volatility. How much the price has been swinging recently. Higher means choppier.',
  return_1d: "Yesterday's daily percent return. Captures recent single-day momentum.",
  volume: 'Shares traded. Spikes often line up with big news or a shift in trend.',
}

export default function PredictTab({symbol}) {
  const [data,setData]= useState(null)
  const [loading,setLoading]= useState(false)
  const [error,setError]= useState(null)
  const [openFeature,setOpenFeature] = useState(null)
  useEffect(()=>{
    if (!symbol) return
    setLoading(true); setError(null); setData(null)
    getPrediction(symbol)
      .then(setData)
      .catch(()=>setError('not enough history to train on this ticker'))
      .finally(()=>setLoading(false))
  },[symbol])
  useEffect(()=>{
    const closeAll= ()=> setOpenFeature(null)
    window.addEventListener('click',closeAll)
    return ()=> window.removeEventListener('click',closeAll)
  },[])

  if (!symbol) return <div className="empty-state">search a ticker to run predictions</div>
  if (loading) return <div className="empty-state">training models on {symbol}...</div>
  if (error) return <div className="empty-state">{error}</div>
  if (!data) return null
  const maxImpact= Math.max(...data.xgb_explanation.map(f=>Math.abs(f.impact)))
  function toggleFeature(key,e) {
    e.stopPropagation()
    setOpenFeature(prev=> prev===key ? null : key)
  }
  
  return (
    <div className="predict-tab">
      <div className="last-close-banner">
        <span className="label">Last Close</span>
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
      <p className="explain-note">Positive bars push the price up, negative bars pull it down; sorted by strength.</p>
      <div className="feature-list">
        {data.xgb_explanation.map(f=>{
          const up= f.impact>=0
          const barWidth= (Math.abs(f.impact)/maxImpact)*100
          const isOpen= openFeature===f.feature
          return (
            <div key={f.feature} className="feature-row">
              <button className="feature-name-btn" onClick={e=>toggleFeature(f.feature,e)}>
                {FEATURE_NAMES[f.feature] || f.feature} <span className="mono feature-key">({f.feature})</span>
              </button>
 
              <div className="feature-row-bar">
                <div className="feature-bar-track">
                  <div
                    className="feature-bar-fill"
                    style={{width:`${barWidth}%`,background:up?'var(--up)':'var(--down)'}}
                  />
                </div>
                <span className="mono feature-value" style={{color:up?'var(--up)':'var(--down)'}}>
                  {up?'+':''}{f.impact.toFixed(2)}
                </span>
              </div>
 
              {isOpen && FEATURE_INFO[f.feature] && (
                <div className="feature-drawer" onClick={e=>e.stopPropagation()}>
                  {FEATURE_INFO[f.feature]}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}