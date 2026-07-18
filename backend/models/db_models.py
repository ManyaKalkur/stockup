from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class Ticker(Base):
	__tablename__= "tickers"
	id= Column(Integer,primary_key=True)
	symbol= Column(String,unique=True,index=True,nullable=False)
	name= Column(String)
	sector= Column(String)
	indexed_at= Column(DateTime(timezone=True),server_default=func.now())

class PriceHistory(Base):
	__tablename__= "price_history"
	id= Column(Integer,primary_key=True)
	ticker_id= Column(Integer,ForeignKey("tickers.id"),index=True)
	date= Column(DateTime,index=True)
	open= Column(Float)
	high= Column(Float)
	low= Column(Float)
	close= Column(Float)
	volume= Column(Float)

class Prediction(Base):
	__tablename__= "predictions"
	id= Column(Integer,primary_key=True)
	ticker_id= Column(Integer,ForeignKey("tickers.id"),index=True)
	model_name= Column(String)
	predicted_at= Column(DateTime(timezone=True),server_default=func.now())
	target_date= Column(DateTime)
	predicted_price= Column(Float)
	actual_price= Column(Float,nullable=True)
	confidence= Column(Float,nullable=True)

class WatchlistItem(Base):
	__tablename__= "watchlist"
	id= Column(Integer,primary_key=True)
	user_id= Column(String,index=True)
	ticker_id= Column(Integer,ForeignKey("tickers.id"))
	added_at= Column(DateTime(timezone=True),server_default=func.now())