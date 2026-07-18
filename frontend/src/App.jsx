import { useState, useEffect } from 'react'
import './theme.css'
import './app.css'
import TickerTape from './components/TickerTape'
import SearchBar from './components/SearchBar'
import ThemeToggle from './components/ThemeToggle'
import ChartTab from './components/tabs/ChartTab'
import PredictTab from './components/tabs/PredictTab'
import AskTab from './components/tabs/AskTab'
import ReportTab from './components/tabs/ReportTab'

const TABS= ['Chart','Predict','Ask','Report']

export default function App() {
  const [theme,setTheme]= useState('dark')
  const [symbol,setSymbol]= useState(null)
  const [tab,setTab]= useState('Chart')
  useEffect(()=>{
    document.documentElement.setAttribute('data-theme',theme)
  },[theme])
  return (
    <div>
      <TickerTape/>
      <header className="app-header">
        <h1>Stock<span style={{color:'var(--amber)'}}>Up</span></h1>
        <SearchBar onSelect={s=>{setSymbol(s); setTab('Chart')}}/>
        <ThemeToggle theme={theme} setTheme={setTheme}/>
      </header>

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
      </main>
    </div>
  )
}