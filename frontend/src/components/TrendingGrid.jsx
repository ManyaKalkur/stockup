const TRENDING= ['AAPL','NVDA','TSLA','MSFT','AMZN','GOOGL','META','AMD']

export default function TrendingGrid({prices,onSelect}) {
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