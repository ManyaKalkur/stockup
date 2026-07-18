import pandas as pd

def add_indicators(df:pd.DataFrame):
	df = df.copy()
	df["sma_10"]= df["close"].rolling(10).mean()
	df["sma_30"]= df["close"].rolling(30).mean()
	df["ema_10"]= df["close"].ewm(span=10).mean()
	delta= df["close"].diff()
	gain= delta.clip(lower=0).rolling(14).mean()
	loss= -delta.clip(upper=0).rolling(14).mean()
	rs= gain/loss.replace(0,1e-9)
	df["rsi_14"]= 100-(100/(1+rs))
	ema_12= df["close"].ewm(span=12).mean()
	ema_26= df["close"].ewm(span=26).mean()
	df["macd"]= ema_12-ema_26
	df["macd_signal"]= df["macd"].ewm(span=9).mean()
	df["volatility_10"]= df["close"].rolling(10).std()
	df["return_1d"]= df["close"].pct_change()
	return df.dropna()