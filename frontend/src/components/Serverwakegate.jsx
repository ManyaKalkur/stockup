import { useEffect, useRef, useState } from 'react'
import { pingHealth } from '../api'

export default function ServerWakeGate({children}) {
  const [ready,setReady]= useState(false)
  const [slow,setSlow]= useState(false)
  const attempts= useRef(0)
  useEffect(()=>{
    let cancelled= false
    const slowTimer= setTimeout(()=>{ if (!cancelled) setSlow(true) },4000)
    async function poll() {
      try {
        await pingHealth()
        if (!cancelled) setReady(true)
      } catch {
        attempts.current+= 1
        if (!cancelled) setTimeout(poll,2000)
      }
    }
    poll()
    return ()=>{ cancelled=true; clearTimeout(slowTimer) }
  },[])
  if (ready) return children
  return (
    <div className="wake-gate">
      <div className="wake-spinner"/>
      <p className="mono">{slow ?'Waking the server up: First load can take ~30-60s':'connecting...'}</p>
    </div>
  )
}