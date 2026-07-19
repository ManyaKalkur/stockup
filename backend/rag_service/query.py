from groq import Groq
from core.config import settings
from rag_service.embed import embed_query
from rag_service.pinecone_client import get_index

_client= None
def get_client():
	global _client
	if _client is None:
		_client= Groq(api_key=settings.GROQ_API_KEY)
	return _client

def ask(symbol:str, question:str, top_k=6):
	index= get_index()
	q_emb= embed_query(question)
	results= index.query(vector=q_emb,top_k=top_k,namespace=symbol.upper(),include_metadata=True)
	matches= results.get("matches",[])
	if not matches:
		return {"answer":"no indexed data for this symbol yet, try ingesting first","sources":[]}
	context_blocks= []
	sources= []
	for m in matches:
		meta= m["metadata"]
		context_blocks.append(f"[{meta['source']} - {meta['date']}] {meta['text']}")
		sources.append({"source":meta["source"],"url":meta["url"],"date":meta["date"]})
	context= "\n\n".join(context_blocks)
	prompt= f"""you're a financial analyst assistant. answer the question about {symbol} using only the context below. cite which source you're drawing from inline. if the context doesn't answer it, say so.
context:
{context}
question: {question}"""
	response= get_client().chat.completions.create(
		model="llama-3.3-70b-versatile",
		max_tokens=600,
		messages=[{"role":"user","content":prompt}],
	)
	answer= response.choices[0].message.content
	return {"answer":answer,"sources":sources}