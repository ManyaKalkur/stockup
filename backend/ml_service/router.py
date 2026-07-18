from fastapi import APIRouter, HTTPException
from data_service.prices import fetch_price_history
from ml_service.xgb_model import train_xgb
from ml_service.lstm_model import train_lstm
from ml_service.explain import explain_xgb

router= APIRouter()

@router.get("/predict/{symbol}")
def predict(symbol:str, period:str="1y"):
	rows= fetch_price_history(symbol,period=period)
	if len(rows) < 60:
		raise HTTPException(400,"not enough history to train on")
	xgb_result= train_xgb(rows)
	lstm_result= train_lstm(rows)
	if not xgb_result or not lstm_result:
		raise HTTPException(400,"not enough clean data after feature engineering")
	explanation= explain_xgb(xgb_result["model"], xgb_result["features"])

	return {
		"symbol": symbol.upper(),
		"last_close": xgb_result["last_close"],
		"xgb_prediction": xgb_result["prediction"],
		"lstm_prediction": lstm_result["prediction"],
		"xgb_explanation": explanation,
	}