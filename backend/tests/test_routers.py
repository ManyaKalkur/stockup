from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client= TestClient(app)

def test_ask_endpoint_returns_answer():
	fake_result= {"answer":"prices rose on strong demand","sources":[]}
	with patch("rag_service.router.ask",return_value=fake_result):
		resp= client.get("/api/rag/ask/AAPL",params={"question":"why did it move"})
	assert resp.status_code== 200
	assert resp.json()["answer"]== "prices rose on strong demand"

def test_ingest_endpoint_returns_404_for_unknown_ticker():
	with patch("rag_service.router.get_or_create_ticker",return_value=None):
		resp= client.post("/api/rag/ingest/ZZZZ")
	assert resp.status_code== 404

def test_ingest_endpoint_returns_chunk_count():
	fake_ticker= MagicMock(name="AAPL")
	with patch("rag_service.router.get_or_create_ticker",return_value=fake_ticker),\
	     patch("rag_service.router.ingest_symbol",return_value=12):
		resp= client.post("/api/rag/ingest/AAPL")
	assert resp.status_code== 200
	assert resp.json()["chunks_indexed"]== 12

def test_report_endpoint_returns_400_on_error():
	with patch("agent_service.router.generate_report",return_value={"error":"not enough price history for this symbol"}):
		resp= client.get("/api/agent/report/ZZZZ")
	assert resp.status_code== 400

def test_report_endpoint_returns_summary():
	fake_result= {"symbol":"AAPL","summary":"stable outlook","last_close":150.0,"predictions":{},"top_features":[]}
	with patch("agent_service.router.generate_report",return_value=fake_result):
		resp= client.get("/api/agent/report/AAPL")
	assert resp.status_code== 200
	assert resp.json()["summary"]== "stable outlook"