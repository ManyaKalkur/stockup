import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.config import settings
from core.cache import cached

@retry(
	stop=stop_after_attempt(3),
	wait=wait_exponential(multiplier=1,min=1,max=6),
	retry=retry_if_exception_type(requests.exceptions.RequestException),
)
def _get(url:str,params:dict):
	resp= requests.get(url,params=params,timeout=10)
	resp.raise_for_status()
	return resp

@cached(ttl_seconds=300)
def fetch_news(company_name:str, limit=15):
	url= "https://newsapi.org/v2/everything"
	params= {
		"q": company_name,
		"sortBy": "publishedAt",
		"language": "en",
		"pageSize": limit,
		"apiKey": settings.NEWSAPI_KEY,
	}
	try:
		resp= _get(url,params)
	except requests.exceptions.RequestException:
		return []
	articles= resp.json().get("articles",[])
	return [{
		"text": f"{a['title']}. {a.get('description') or ''}",
		"source": a["source"]["name"],
		"url": a["url"],
		"date": a["publishedAt"],
	} for a in articles]