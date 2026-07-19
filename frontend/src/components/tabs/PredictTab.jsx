import { useEffect, useState } from 'react'
import { getPrediction } from '../../api'
const LABELS= {
  xgboost: 'XGBoost',
  random_forest: 'Random Forest',
  linear_regression: 'Linear Regression',
  svm: 'SVM',
}
const FEATURE_INFO= {
  sma_10: '10-Day Simple Moving Average (SMA). This is the average stock price over the last 10 days. It smooths out daily ups and downs to show the short-term trend. If the current price is above this line, the stock is generally moving upward.',
  sma_30: '30-Day Simple Moving Average (SMA). This is the average stock price over the last 30 days. It reflects the longer-term trend. When the price moves above or below this average, it can indicate a significant change in direction.',
  ema_10: '10-Day Exponential Moving Average (EMA). Similar to the moving average, but it gives more importance to recent prices. This makes it react faster to market changes than a Simple Moving Average.',
  rsi_14: '14-Day Relative Strength Index (RSI). A momentum indicator that ranges from 0 to 100. Values above 70 may mean the stock has risen too quickly (overbought), while values below 30 may mean it has fallen too much (oversold).',
  macd: 'Moving Average Convergence Divergence (MACD). A momentum indicator that compares two moving averages to show whether bullish or bearish momentum is strengthening or weakening.',
  macd_signal: 'MACD Signal Line. This is a smoothed version of the MACD. When the MACD crosses above the signal line, it may suggest upward momentum. Crossing below may suggest downward momentum.',
  volatility_10: '10-Day Volatility. Measures how much the stock price has been changing over the last 10 days. Higher volatility means larger price swings and greater uncertainty.',
  return_1d: "1-Day Return. The percentage change in the stock's price compared with the previous trading day. It shows whether the stock gained or lost value yesterday.",
  volume: 'Trading Volume. The total number of shares traded during the day. High trading volume usually means strong investor interest and often accompanies important price movements.'
};

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
              {FEATURE_INFO[f.feature] && <p className="feature-desc">{FEATURE_INFO[f.feature]}</p>}
            </div>
          )
        })}
      </div>
    </div>
  )
}