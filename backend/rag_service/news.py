import requests
from core.config import settings

def fetch_news(company_name:str, limit=15):
	url= "https://newsapi.org/v2/everything"
	params= {
		"q": company_name,
		"sortBy": "publishedAt",
		"language": "en",
		"pageSize": limit,
		"apiKey": settings.NEWSAPI_KEY,
	}
	resp= requests.get(url,params=params,timeout=10)
	resp.raise_for_status()
	articles= resp.json().get("articles",[])
	return [{
		"text": f"{a['title']}. {a.get('description') or ''}",
		"source": a["source"]["name"],
		"url": a["url"],
		"date": a["publishedAt"],
	} for a in articles]