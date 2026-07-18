import uuid
from rag_service.news import fetch_news
from rag_service.filings import fetch_recent_filings, fetch_filing_text
from rag_service.embed import embed_texts
from rag_service.pinecone_client import get_index

def chunk_text(text:str, size=800, overlap=100):
	chunks= []
	i= 0
	while i<len(text):
		chunks.append(text[i:i+size])
		i+= size-overlap
	return chunks

def ingest_symbol(symbol:str, company_name:str):
	index= get_index()
	items= []
	for article in fetch_news(company_name):
		items.append({"text":article["text"],"source":article["source"],"url":article["url"],"date":article["date"],"type":"news"})
	for filing in fetch_recent_filings(symbol):
		text= fetch_filing_text(filing["url"])
		for chunk in chunk_text(text):
			items.append({"text":chunk,"source":filing["form"],"url":filing["url"],"date":filing["date"],"type":"filing"})
	if not items:
		return 0
	texts= [i["text"] for i in items]
	embeddings= embed_texts(texts)
	vectors= []
	for item,emb in zip(items,embeddings):
		vectors.append({
			"id": str(uuid.uuid4()),
			"values": emb,
			"metadata": {**item,"symbol":symbol.upper()},
		})
	index.upsert(vectors=vectors,namespace=symbol.upper())
	return len(vectors)