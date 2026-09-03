from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from data_service.prices import fetch_price_history, get_or_create_ticker
from rag_service.ingest import ingest_symbol
from rag_service.query import ask

router = APIRouter()

@router.post("/ingest/{symbol}")
def ingest(symbol:str, db:Session=Depends(get_db)):
	try:
		ticker= get_or_create_ticker(db,symbol)
	except SQLAlchemyError:
		db.rollback()
		ticker= None
	if ticker:
		company_name= ticker.name
	else:
		if not fetch_price_history(symbol,period="1mo"):
			raise HTTPException(404,f"couldn't find {symbol}")
		company_name= symbol.upper()
	count = ingest_symbol(symbol,company_name)
	return {"symbol":symbol.upper(),"chunks_indexed":count}

@router.get("/ask/{symbol}")
def ask_endpoint(symbol:str, question:str):
	return ask(symbol,question)