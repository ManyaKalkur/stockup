import yfinance as yf
from sqlalchemy.orm import Session
from models.db_models import Ticker, PriceHistory

def search_ticker(query:str):
	# yfinance has no clean search api, use Ticker.info as a lookup/validate step
	try:
		t= yf.Ticker(query)
		info= t.info
		if not info or info.get("regularMarketPrice") is None:
			return None
		return {
			"symbol": query.upper(),
			"name": info.get("shortName",query),
			"sector": info.get("sector","unknown"),
		}
	except Exception:
		return None

def get_or_create_ticker(db:Session, symbol:str):
	ticker= db.query(Ticker).filter(Ticker.symbol==symbol.upper()).first()
	if ticker:
		return ticker
	meta= search_ticker(symbol)
	if not meta:
		return None
	ticker = Ticker(symbol=meta["symbol"],name=meta["name"],sector=meta["sector"])
	db.add(ticker)
	db.commit()
	db.refresh(ticker)
	return ticker

def fetch_price_history(symbol:str,period="6mo",interval="1d"):
	t= yf.Ticker(symbol)
	hist= t.history(period=period,interval=interval)
	if hist.empty:
		return []
	hist= hist.reset_index()
	rows= []
	for _,row in hist.iterrows():
		rows.append({
			"date": row["Date"],
			"open": row["Open"],
			"high": row["High"],
			"low": row["Low"],
			"close": row["Close"],
			"volume": row["Volume"],
		})
	return rows

def cache_price_history(db:Session, ticker:Ticker, rows:list):
	existing_dates= {p.date for p in db.query(PriceHistory).filter(PriceHistory.ticker_id==ticker.id).all()}
	new_rows= [r for r in rows if r["date"] not in existing_dates]
	for r in new_rows:
		db.add(PriceHistory(ticker_id=ticker.id,**r))
	db.commit()
	return len(new_rows)