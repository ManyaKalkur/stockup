from unittest.mock import patch, MagicMock
import requests
from rag_service.filings import get_cik, fetch_recent_filings, fetch_filing_text

def test_get_cik_parses_cik_from_response():
	resp= MagicMock()
	resp.text= "some xml ... CIK=0000320193&owner=include ... "
	with patch("rag_service.filings._get",return_value=resp):
		cik= get_cik("AAPL")
	assert cik== "0000320193"

def test_get_cik_returns_none_when_not_found():
	resp= MagicMock()
	resp.text= "no cik here"
	with patch("rag_service.filings._get",return_value=resp):
		assert get_cik("ZZZZ") is None

def test_get_cik_returns_none_on_network_failure():
	with patch("rag_service.filings._get",side_effect=requests.exceptions.RequestException("down")):
		assert get_cik("AAPL") is None

def test_fetch_recent_filings_filters_to_known_forms():
	fake_cik_resp= MagicMock()
	fake_cik_resp.text= "CIK=0000320193&x"
	fake_submissions= MagicMock()
	fake_submissions.json.return_value= {
		"filings": {"recent": {
			"form": ["10-K","4","10-Q"],
			"filingDate": ["2026-01-01","2026-01-02","2026-01-03"],
			"accessionNumber": ["0000320193-26-000001","0000320193-26-000002","0000320193-26-000003"],
			"primaryDocument": ["a.htm","b.htm","c.htm"],
		}}
	}

	with patch("rag_service.filings._get",side_effect=[fake_cik_resp,fake_submissions]):
		filings= fetch_recent_filings("AAPL")
	forms= [f["form"] for f in filings]
	assert "10-K" in forms
	assert "10-Q" in forms
	assert "4" not in forms

def test_fetch_filing_text_strips_html():
	resp= MagicMock()
	resp.text= "<html><body><p>Risk factors include competition.</p></body></html>"
	with patch("rag_service.filings._get",return_value=resp):
		text= fetch_filing_text("http://example.com/filing.htm")
	assert "Risk factors include competition." in text
	assert "<p>" not in text

def test_fetch_filing_text_returns_empty_on_failure():
	with patch("rag_service.filings._get",side_effect=requests.exceptions.RequestException("down")):
		assert fetch_filing_text("http://example.com/filing.htm")== ""