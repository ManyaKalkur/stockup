import asyncio
import logging
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db
from data_service.prices import get_or_create_ticker, fetch_price_history, cache_price_history, serialize_price_rows
from data_service.live import manager, price_poll_loop

router= APIRouter()
logger= logging.getLogger(__name__)

@router.get("/search/{symbol}")
def search(symbol:str, db:Session=Depends(get_db)):
	ticker= get_or_create_ticker(db,symbol)
	if not ticker:
		raise HTTPException(404,f"couldn't find {symbol}")
	return {"symbol":ticker.symbol,"name":ticker.name,"sector":ticker.sector}

@router.get("/prices/{symbol}")
def prices(symbol:str, period:str="6mo", db:Session=Depends(get_db)):
	rows= fetch_price_history(symbol,period=period)
	if not rows:
		raise HTTPException(404,f"couldn't find price history for {symbol}")
	try:
		ticker= get_or_create_ticker(db,symbol)
		if ticker:
			cache_price_history(db,ticker,rows)
	except SQLAlchemyError:
		db.rollback()
		logger.exception("Could not cache price history for %s",symbol)
	return {"symbol":symbol.upper(),"rows":serialize_price_rows(rows)}

@router.websocket("/ws/{symbol}")
async def price_ws(ws:WebSocket, symbol:str):
	symbol= symbol.upper()
	is_first= symbol not in manager.active
	await manager.connect(symbol,ws)
	if is_first:
		asyncio.create_task(price_poll_loop(symbol))
	try:
		while True:
			await ws.receive_text()
	except WebSocketDisconnect:
		manager.disconnect(symbol,ws)