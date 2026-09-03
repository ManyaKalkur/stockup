import { useState, useEffect } from 'react'
import './theme.css'
import './app.css'
import TickerTape from './components/TickerTape'
import SearchBar from './components/SearchBar'
import ThemeToggle from './components/ThemeToggle'
import ServerWakeGate from './components/ServerWakeGate'
import ChartTab from './components/tabs/ChartTab'
import PredictTab from './components/tabs/PredictTab'
import AskTab from './components/tabs/AskTab'
import ReportTab from './components/tabs/ReportTab'
import TrendingGrid from './components/TrendingGrid'
import TrackRecordTab from './components/tabs/TrackRecordTab'

const TABS= ['Chart','Predict','Ask','Report','Track Record']
const SYMBOL_KEY= 'stockup-selected-symbol'
const TAB_KEY= 'stockup-selected-tab'
function savedTab() {
  const tab= localStorage.getItem(TAB_KEY)
  return TABS.includes(tab) ? tab : 'Chart'
}
export default function App() {
  const [theme,setTheme]= useState('dark')
  const [symbol,setSymbol]= useState(()=>localStorage.getItem(SYMBOL_KEY))
  const [tab,setTab]= useState(savedTab)
  useEffect(()=>{
    document.documentElement.setAttribute('data-theme',theme)
  },[theme])
  useEffect(()=>{
    if (symbol) localStorage.setItem(SYMBOL_KEY,symbol)
    else localStorage.removeItem(SYMBOL_KEY)
  },[symbol])
  useEffect(()=>{
    localStorage.setItem(TAB_KEY,tab)
  },[tab])
  return (
    <div>
      <ServerWakeGate>
        <TickerTape/>
        <header className="app-header">
          <h1>Stock<span style={{color:'var(--amber)'}}>Up</span></h1>
          <SearchBar onSelect={s=>{setSymbol(s); setTab('Chart')}}/>
          <ThemeToggle theme={theme} setTheme={setTheme}/>
        </header>
        {symbol?(
          <>
            <nav className="tab-bar">
              {TABS.map(t=>(
                <button key={t} className={tab===t?'tab active':'tab'} onClick={()=>setTab(t)}>{t}</button>
              ))}
            </nav>
            <main className="app-main">
              {tab==='Chart' && <ChartTab symbol={symbol}/>}
              {tab==='Predict' && <PredictTab symbol={symbol}/>}
              {tab==='Ask' && <AskTab symbol={symbol}/>}
              {tab==='Report' && <ReportTab symbol={symbol}/>}
              {tab==='Track Record' && <TrackRecordTab symbol={symbol}/>}
            </main>
          </>
        ):(
          <main className="app-main">
            <TrendingGrid onSelect={s=>{setSymbol(s); setTab('Chart')}}/>
          </main>
        )}
      </ServerWakeGate>
    </div>
  )
}