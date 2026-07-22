import { useEffect, useState } from 'react'
import { liveSocket } from '../api'

const TRENDING= ['AAPL','NVDA','TSLA','MSFT','AMZN','GOOGL','META','AMD']

export default function TrendingGrid({onSelect}) {
  const [prices,setPrices]= useState({})
  useEffect(()=>{
    const sockets= TRENDING.map(symbol=>{
      const ws= liveSocket(symbol)
      ws.onmessage= (e)=>{
        const data= JSON.parse(e.data)
        setPrices(prev=>({...prev,[symbol]:{price:data.price,prevPrice:prev[symbol]?.price}}))
      }
      return ws
    })
    return ()=> sockets.forEach(ws=>ws.close())
  },[])

  return (
    <div className="trending-wrap">
      <h2>Trending Stocks</h2>
      <p className="explain-note">Tap a stock to see its chart, predictions, and news</p>
      <div className="trending-grid">
        {TRENDING.map(symbol=>{
          const p= prices[symbol]
          const up= p && p.prevPrice!=null? p.price>=p.prevPrice:true
          return (
            <button key={symbol} className="trending-card" onClick={()=>onSelect(symbol)}>
              <span className="mono trending-symbol">{symbol}</span>
              <span className="mono trending-price" style={{color:up?'var(--up)':'var(--down)'}}>
                {p ? `$${p.price.toFixed(2)}` : '—'}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}