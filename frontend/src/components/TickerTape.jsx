import { useEffect, useState } from 'react'
import { liveSocket } from '../api'

const TAPE_SYMBOLS= ['AAPL','NVDA','TSLA','MSFT','AMZN','GOOGL']
const STREAMED_SYMBOLS= [...TAPE_SYMBOLS,'META','AMD']

export default function TickerTape({onPricesChange}) {
  const [prices,setPrices]= useState({})

  useEffect(()=>{
    onPricesChange(prices)
  },[onPricesChange,prices])
  useEffect(()=>{
    const sockets= STREAMED_SYMBOLS.map(symbol=>{
      const ws= liveSocket(symbol)
      ws.onmessage= (e)=>{
        const data= JSON.parse(e.data)
        setPrices(prev=>({...prev,[symbol]:{price:data.price,prevPrice:prev[symbol]?.price}}))
      }
      return ws
    })
    return ()=> sockets.forEach(ws=>{
      ws.onmessage= null
      if (ws.readyState===WebSocket.OPEN) ws.close()
      else if (ws.readyState===WebSocket.CONNECTING) ws.onopen= ()=>ws.close()
    })
  },[onPricesChange])

  const renderItems= (prefix)=> TAPE_SYMBOLS.map(symbol=>{
    const p= prices[symbol]
    const up= p && p.prevPrice!=null? p.price>=p.prevPrice: true
    return (
      <span key={`${prefix}-${symbol}`} className="ticker-item mono">
        {symbol} <span className="ticker-price" style={{color:up?'var(--up)':'var(--down)'}}>{p? p.price.toFixed(2):'N/A'}</span>
      </span>
    )
  })

  return (
    <div className="ticker-tape">
      <div className="ticker-track">{renderItems('a')}{renderItems('b')}</div>
    </div>
  )
}