from unittest.mock import patch, MagicMock
from rag_service.ingest import chunk_text, ingest_symbol

def test_chunk_text_splits_with_overlap():
	text= "a"*2000
	chunks= chunk_text(text,size=800,overlap=100)
	assert len(chunks)>1
	assert all(len(c)<= 800 for c in chunks)

def test_chunk_text_handles_short_text():
	chunks= chunk_text("short text")
	assert chunks== ["short text"]

def test_ingest_symbol_returns_zero_when_nothing_found():
	with patch("rag_service.ingest.get_index",return_value=MagicMock()),\
	     patch("rag_service.ingest.fetch_news",return_value=[]),\
	     patch("rag_service.ingest.fetch_recent_filings",return_value=[]):
		count= ingest_symbol("NOPE","No Company")
	assert count== 0

def test_ingest_symbol_upserts_news_and_filing_chunks():
	fake_index= MagicMock()
	fake_news= [{"text":"news chunk","source":"Reuters","url":"http://x.com","date":"2026-01-01"}]
	fake_filings= [{"form":"10-K","date":"2026-01-01","url":"http://sec.gov/filing.htm"}]
	with patch("rag_service.ingest.get_index",return_value=fake_index),\
	     patch("rag_service.ingest.fetch_news",return_value=fake_news),\
	     patch("rag_service.ingest.fetch_recent_filings",return_value=fake_filings),\
	     patch("rag_service.ingest.fetch_filing_text",return_value="some filing text"),\
	     patch("rag_service.ingest.embed_texts",return_value=[[0.1]]*2):
		count= ingest_symbol("AAPL","Apple Inc.")
	assert count== 2
	fake_index.upsert.assert_called_once()
	_,kwargs= fake_index.upsert.call_args
	assert kwargs["namespace"]== "AAPL"
	assert len(kwargs["vectors"])== 2