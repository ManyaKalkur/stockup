import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { getPrices, liveSocket } from '../../api'

export default function ChartTab({symbol}) {
  const [rows,setRows]= useState([])
  const [live,setLive]= useState(null)
  const [loading,setLoading]= useState(true)

  useEffect(()=>{
    if (!symbol) return
    setLoading(true)
    getPrices(symbol).then(data=>{
      setRows(data.rows.map(r=>({date:r.date.slice(0,10),close:r.close})))
      setLoading(false)
    }).catch(()=>setLoading(false))

    const ws = liveSocket(symbol)
    ws.onmessage= e=> setLive(JSON.parse(e.data).price)
    return ()=> ws.close()
  },[symbol])

  if (!symbol) return <div className="empty-state">search a ticker to see its chart</div>
  if (loading) return <div className="empty-state">loading {symbol}...</div>
  const last= rows[rows.length-1]
  const up= last && live!=null ? live>=last.close : true

  return (
    <div className="chart-tab">
      <div className="chart-header">
        <h2 className="mono">{symbol}</h2>
        {live!=null && <span className="mono live-price" style={{color:up?'var(--up)':'var(--down)'}}>${live.toFixed(2)}</span>}
      </div>
      <ResponsiveContainer width="100%" height={360}>
        <LineChart data={rows}>
          <CartesianGrid stroke="var(--border)" strokeDasharray="3 3"/>
          <XAxis dataKey="date" stroke="var(--text-dim)" fontSize={11} minTickGap={40}/>
          <YAxis stroke="var(--text-dim)" fontSize={11} domain={['auto','auto']}/>
          <Tooltip contentStyle={{background:'var(--surface)',border:'1px solid var(--border)',borderRadius:8}}/>
          <Line type="monotone" dataKey="close" stroke="var(--amber)" strokeWidth={2} dot={false}/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}