import { useEffect, useState } from 'react'
import { liveSocket } from '../api'

const WATCHLIST= ['AAPL','NVDA','TSLA','MSFT','AMZN','GOOGL']

export default function TickerTape() {
  const [prices,setPrices]= useState({})

  useEffect(()=>{
    const sockets= WATCHLIST.map(symbol=>{
      const ws= liveSocket(symbol)
      ws.onmessage= (e)=>{
        const data= JSON.parse(e.data)
        setPrices(prev=>({...prev,[symbol]:{price:data.price,prevPrice:prev[symbol]?.price}}))
      }
      return ws
    })
    return ()=> sockets.forEach(ws=>ws.close())
  },[])

  const renderItems= (prefix)=> WATCHLIST.map(symbol=>{
    const p= prices[symbol]
    const up= p && p.prevPrice!=null? p.price>=p.prevPrice: true
    return (
      <span key={`${prefix}-${symbol}`} className="ticker-item mono">
        {symbol} <span style={{color:up?'var(--up)':'var(--down)'}}>{p? p.price.toFixed(2) : 'N/A'}</span>
      </span>
    )
  })

  return (
    <div className="ticker-tape">
      <div className="ticker-track">{renderItems('a')}{renderItems('b')}</div>
    </div>
  )
}