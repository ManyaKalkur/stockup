import requests
from core.config import settings

HEADERS= {"User-Agent": settings.SEC_EDGAR_USER_AGENT}

def get_cik(symbol:str):
	url= "https://www.sec.gov/cgi-bin/browse-edgar"
	params= {"action":"getcompany","company":symbol,"type":"10-K","dateb":"","owner":"include","count":"1","output":"atom"}
	resp= requests.get(url,params=params,headers=HEADERS,timeout=10)
	if resp.status_code != 200 or "CIK=" not in resp.text:
		return None
	start= resp.text.find("CIK=")+4
	return resp.text[start:start+10].split("&")[0]

def fetch_recent_filings(symbol:str, limit=5):
	cik= get_cik(symbol)
	if not cik:
		return []
	cik_padded= cik.zfill(10)
	url= f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
	resp= requests.get(url,headers=HEADERS,timeout=10)
	if resp.status_code != 200:
		return []
	recent= resp.json().get("filings",{}).get("recent",{})
	forms= recent.get("form",[])
	dates= recent.get("filingDate",[])
	accns= recent.get("accessionNumber",[])
	docs= recent.get("primaryDocument",[])
	filings= []
	for form,date,accn,doc in zip(forms,dates,accns,docs):
		if form not in ("10-K","10-Q","8-K"):
			continue
		accn_clean= accn.replace("-","")
		filing_url= f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn_clean}/{doc}"
		filings.append({"form":form,"date":date,"url":filing_url})
		if len(filings)>=limit:
			break
	return filings

def fetch_filing_text(filing_url:str, max_chars=8000):
	from bs4 import BeautifulSoup
	resp= requests.get(filing_url,headers=HEADERS,timeout=15)
	if resp.status_code != 200:
		return ""
	soup= BeautifulSoup(resp.text,"html.parser")
	text= soup.get_text(separator=" ",strip=True)
	return text[:max_chars]