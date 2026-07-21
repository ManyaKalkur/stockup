import yfinance as yf
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential
from core.cache import cached
from models.db_models import Ticker, PriceHistory
 
RETRY= dict(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=1,min=1,max=6))
@retry(**RETRY)
def _fetch_info(query:str):
	return yf.Ticker(query).info
@retry(**RETRY)
def _fetch_history(symbol:str,period:str,interval:str):
	return yf.Ticker(symbol).history(period=period,interval=interval)

def search_ticker(query:str):
	# yfinance has no clean search api, use Ticker.info as a lookup/validate step
	try:
		info= _fetch_info(query)
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
	try:
		hist= _fetch_history(symbol,period,interval)
	except Exception:
		return []
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