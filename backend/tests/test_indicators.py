import pandas as pd
from ml_service.indicators import add_indicators
from tests.helpers import make_rows

def test_indicators_add_expected_columns():
	df= pd.DataFrame(make_rows())
	out= add_indicators(df)
	for col in ["sma_10","sma_30","ema_10","rsi_14","macd","macd_signal","volatility_10","return_1d"]:
		assert col in out.columns

def test_indicators_drop_nan_rows():
	df= pd.DataFrame(make_rows())
	out= add_indicators(df)
	assert not out.isnull().values.any()

def test_indicators_shrink_length():
	df= pd.DataFrame(make_rows(60))
	out= add_indicators(df)
	assert len(out)<len(df)