from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from data_service.prices import fetch_price_history, get_or_create_ticker
from core.cache import cached
from core.database import get_db, SessionLocal

router= APIRouter()

@cached(ttl_seconds=120)
def _run_predictions(symbol:str, period:str):
	from ml_service.models import train_all
	from ml_service.explain import explain_model
	from ml_service.tracking import log_predictions
	rows= fetch_price_history(symbol,period=period)
	if len(rows) < 60:
		return None
	result= train_all(rows)
	if not result:
		return None
	explanation= explain_model(result["xgb_model"], result["xgb_features"])
	db= SessionLocal()
	try:
		ticker= get_or_create_ticker(db,symbol)
		if ticker:
			log_predictions(db,ticker.id,result["predictions"])
	finally:
		db.close()

	return {
		"symbol": symbol.upper(),
		"last_close": result["last_close"],
		"predictions": result["predictions"],
		"xgb_explanation": explanation,
	}
 
@router.get("/predict/{symbol}")
def predict(symbol:str, period:str="1y"):
	result= _run_predictions(symbol,period)
	if not result:
		raise HTTPException(400,"not enough history to train on")
	return result

@router.get("/accuracy/{symbol}")
def accuracy(symbol:str, db:Session=Depends(get_db)):
	from ml_service.tracking import get_accuracy_summary
	result= get_accuracy_summary(db,symbol)
	if not result:
		raise HTTPException(404,f"couldn't find {symbol}")
	return result