from fastapi import APIRouter, HTTPException
from data_service.prices import fetch_price_history

router= APIRouter()

@router.get("/predict/{symbol}")
def predict(symbol:str, period:str="1y"):
	from ml_service.models import train_all
	from ml_service.explain import explain_model
	rows= fetch_price_history(symbol,period=period)
	if len(rows) < 60:
		raise HTTPException(400,"not enough history to train on")
	result= train_all(rows)
	if not result:
		raise HTTPException(400,"not enough clean data after feature engineering")
	explanation= explain_model(result["xgb_model"], result["xgb_features"])

	return {
		"symbol": symbol.upper(),
		"last_close": result["last_close"],
		"predictions": result["predictions"],
		"xgb_explanation": explanation,
	}