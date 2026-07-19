import pandas as pd
from ml_service.indicators import add_indicators
 
FEATURES= ["sma_10","sma_30","ema_10","rsi_14","macd","macd_signal","volatility_10","return_1d","volume"]
 
def build_dataset(rows:list):
	df= pd.DataFrame(rows)
	df= add_indicators(df)
	df["target"]= df["close"].shift(-1)
	df= df.dropna()
	if len(df)<30:
		return None
	X= df[FEATURES]
	y= df["target"]
	return X, y, float(df["close"].iloc[-1])