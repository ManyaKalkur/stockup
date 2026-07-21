from unittest.mock import patch, MagicMock
import requests
from rag_service.news import fetch_news

def _fake_response():
	resp= MagicMock()
	resp.json.return_value= {
		"articles": [
			{"title":"Company beats earnings","description":"strong quarter","source":{"name":"Reuters"},"url":"http://x.com/1","publishedAt":"2026-01-01T00:00:00Z"},
		]
	}
	return resp

def test_fetch_news_returns_parsed_articles():
	with patch("rag_service.news._get",return_value=_fake_response()):
		articles= fetch_news("UniqueCoOne")
	assert len(articles)== 1
	assert articles[0]["source"]== "Reuters"
	assert "Company beats earnings" in articles[0]["text"]

def test_fetch_news_returns_empty_list_on_network_failure():
	with patch("rag_service.news._get",side_effect=requests.exceptions.RequestException("down")):
		articles= fetch_news("UniqueCoTwo")
	assert articles== []