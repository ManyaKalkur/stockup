from unittest.mock import patch, MagicMock
from agent_service.orchestrator import gather_context, generate_report

def test_gather_context_returns_none_on_insufficient_price_history():
	with patch("agent_service.orchestrator.fetch_price_history",return_value=[{"close":1}]*10):
		assert gather_context("AAPL") is None

def test_gather_context_returns_none_when_training_fails():
	rows= [{"close":100+i,"open":100,"high":101,"low":99,"volume":1000,"date":f"d{i}"} for i in range(100)]
	with patch("agent_service.orchestrator.fetch_price_history",return_value=rows),\
	     patch("ml_service.models.train_all",return_value=None):
		assert gather_context("AAPL") is None

def test_generate_report_returns_error_when_no_context():
	with patch("agent_service.orchestrator.gather_context",return_value=None):
		result= generate_report("AAPL")
	assert "error" in result

def test_generate_report_builds_summary_from_context():
	fake_ctx= {
		"last_close": 150.0,
		"predictions": {"xgboost":151.0,"random_forest":149.5,"linear_regression":150.2,"svm":152.0},
		"top_features": [{"feature":"rsi_14","impact":2.1}],
		"news_context": ["earnings beat expectations"],
	}

	fake_response= MagicMock()
	fake_response.choices= [MagicMock(message=MagicMock(content="AAPL looks stable heading into next week."))]
	fake_client= MagicMock()
	fake_client.chat.completions.create.return_value= fake_response
	with patch("agent_service.orchestrator.gather_context",return_value=fake_ctx),\
	     patch("agent_service.orchestrator.get_client",return_value=fake_client):
		result= generate_report("AAPL")
	assert result["symbol"]== "AAPL"
	assert result["summary"]== "AAPL looks stable heading into next week."
	assert result["last_close"]== 150.0
	assert result["predictions"]["xgboost"] == 151.0