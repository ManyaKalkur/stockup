import importlib
import pandas as pd
from xgboost import XGBRegressor
from ml_service.indicators import add_indicators

FEATURES= ["sma_10","sma_30","ema_10","rsi_14","macd","macd_signal","volatility_10","return_1d","volume"]

def train_xgb(rows:list):
	df= pd.DataFrame(rows)
	df= add_indicators(df)
	df["target"]= df["close"].shift(-1)
	df= df.dropna()
	if len(df)<30:
		return None
	X= df[FEATURES]
	y= df["target"]
	model= XGBRegressor(n_estimators=200,max_depth=4,learning_rate=0.05)
	model.fit(X,y)
	last_row= X.iloc[[-1]]
	pred= float(model.predict(last_row)[0])
	return {"model":model,"prediction":pred,"features":X,"last_close":float(df["close"].iloc[-1])}