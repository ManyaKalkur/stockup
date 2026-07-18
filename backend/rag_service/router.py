from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from data_service.prices import get_or_create_ticker
from rag_service.ingest import ingest_symbol
from rag_service.query import ask

router = APIRouter()

@router.post("/ingest/{symbol}")
def ingest(symbol:str, db:Session=Depends(get_db)):
	ticker = get_or_create_ticker(db,symbol)
	if not ticker:
		raise HTTPException(404,f"couldn't find {symbol}")
	count = ingest_symbol(symbol,ticker.name)
	return {"symbol":symbol.upper(),"chunks_indexed":count}

@router.get("/ask/{symbol}")
def ask_endpoint(symbol:str, question:str):
	return ask(symbol,question)
