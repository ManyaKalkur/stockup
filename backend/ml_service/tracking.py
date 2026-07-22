from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.db_models import Prediction
from data_service.prices import get_or_create_ticker, fetch_price_history
 
def log_predictions(db:Session, ticker_id:int, predictions:dict):
	target_date= datetime.utcnow() + timedelta(days=1)
	for model_name,price in predictions.items():
		db.add(Prediction(
			ticker_id=ticker_id,
			model_name=model_name,
			target_date=target_date,
			predicted_price=price,
		))
	db.commit()
 
def resolve_due_predictions(db:Session, symbol:str, ticker_id:int):
	due= db.query(Prediction).filter(
		Prediction.ticker_id==ticker_id,
		Prediction.actual_price.is_(None),
		Prediction.target_date<=datetime.utcnow(),
	).all()
	if not due:
		return
	rows= fetch_price_history(symbol,period="1mo")
	if not rows:
		return
	for pred in due:
		match= next((r for r in rows if r["date"]>=pred.target_date), None)
		if match:
			pred.actual_price = match["close"]
	db.commit()
	
def get_accuracy_summary(db:Session, symbol:str):
	ticker= get_or_create_ticker(db,symbol)
	if not ticker:
		return None
	resolve_due_predictions(db,symbol,ticker.id)
	resolved= db.query(Prediction).filter(
		Prediction.ticker_id==ticker.id,
		Prediction.actual_price.isnot(None),
	).order_by(Prediction.predicted_at.desc()).all()
	by_model= {}
	for p in resolved:
		by_model.setdefault(p.model_name,[]).append(p)
	summary= {}
	for model_name,preds in by_model.items():
		errors= [abs(p.predicted_price-p.actual_price)/p.actual_price*100 for p in preds]
		summary[model_name]= {
			"count": len(preds),
			"avg_error_pct": round(sum(errors)/len(errors),2),
		}
	recent= [{
		"model": p.model_name,
		"predicted": round(p.predicted_price,2),
		"actual": round(p.actual_price,2),
		"target_date": p.target_date.isoformat(),
	} for p in resolved[:20]]
	return {"symbol":symbol.upper(),"summary":summary,"recent":recent}