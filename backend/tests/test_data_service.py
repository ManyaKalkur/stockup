from unittest.mock import patch
from data_service.prices import search_ticker

def test_search_ticker_returns_none_on_bad_symbol():
	with patch("data_service.prices._fetch_info", side_effect=Exception("not found")):
		assert search_ticker("ZZZZZZ") is None

def test_search_ticker_returns_metadata_on_valid_symbol():
	fake_info= {"regularMarketPrice": 150.0, "shortName": "Apple Inc.", "sector": "Technology"}
	with patch("data_service.prices._fetch_info", return_value=fake_info):
		result = search_ticker("aapl")
		assert result["symbol"]== "AAPL"
		assert result["name"]== "Apple Inc."
		assert result["sector"]== "Technology"

def test_search_ticker_returns_none_when_no_market_price():
	fake_info = {"shortName": "Some Delisted Co"}
	with patch("data_service.prices._fetch_info", return_value=fake_info):
		assert search_ticker("DEAD") is None