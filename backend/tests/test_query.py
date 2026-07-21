from unittest.mock import patch, MagicMock
from rag_service.query import ask

def test_ask_returns_fallback_when_no_matches():
	fake_index= MagicMock()
	fake_index.query.return_value= {"matches":[]}
	with patch("rag_service.query.get_index",return_value=fake_index),\
	     patch("rag_service.query.embed_query",return_value=[0.1,0.2]):
		result= ask("NOPE","why did it move")
	assert result["sources"]== []
	assert "no indexed data" in result["answer"]

def test_ask_returns_grounded_answer_with_sources():
	fake_index= MagicMock()
	fake_index.query.return_value= {
		"matches": [
			{"metadata": {"source":"Reuters","date":"2026-01-01","url":"http://x.com","text":"earnings beat expectations"}},
		]
	}
	fake_groq_response= MagicMock()
	fake_groq_response.choices= [MagicMock(message=MagicMock(content="the stock rose on strong earnings"))]
	fake_client= MagicMock()
	fake_client.chat.completions.create.return_value= fake_groq_response
	with patch("rag_service.query.get_index",return_value=fake_index),\
	     patch("rag_service.query.embed_query",return_value=[0.1,0.2]),\
	     patch("rag_service.query.get_client",return_value=fake_client):
		result= ask("AAPL","why did it move")
	assert result["answer"]== "the stock rose on strong earnings"
	assert result["sources"][0]["source"]== "Reuters"