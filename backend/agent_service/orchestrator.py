from groq import Groq
from core.config import settings
from data_service.prices import fetch_price_history
from rag_service.embed import embed_query
from rag_service.pinecone_client import get_index

_client= None
def get_client():
	global _client
	if _client is None:
		_client= Groq(api_key=settings.GROQ_API_KEY)
	return _client

def gather_context(symbol:str):
	from ml_service.models import train_all
	from ml_service.explain import explain_model
	rows= fetch_price_history(symbol,period="6mo")
	if len(rows)<60:
		return None
	result= train_all(rows)
	if not result:
		return None
	explanation= explain_model(result["xgb_model"], result["xgb_features"])
	index= get_index()
	q_emb= embed_query(f"recent news and events affecting {symbol} stock price")
	results= index.query(vector=q_emb,top_k=8,namespace=symbol.upper(),include_metadata=True)
	news_chunks= [m["metadata"]["text"] for m in results.get("matches",[])]
	return {
		"last_close": result["last_close"],
		"predictions": result["predictions"],
		"top_features": explanation,
		"news_context": news_chunks,
	}

def generate_report(symbol:str):
	ctx= gather_context(symbol)
	if not ctx:
		return {"error":"not enough price history for this symbol"}

	news_block= "\n".join(f"- {c}" for c in ctx["news_context"]) or "no recent indexed news"
	features_block= ", ".join(f"{f['feature']} ({f['impact']})" for f in ctx["top_features"]) or "n/a"
	preds= ctx["predictions"]
	preds_block= "\n".join(f"{name}: {val}" for name,val in preds.items())
	prompt= f"""write a short plain-english market brief for {symbol}. 3-4 sentences max, no headers.

last close: {ctx['last_close']}
model predictions for next close:
{preds_block}
top price-driving features (shap, from xgboost): {features_block}

recent news context:
{news_block}

tie the technical signals and the news together into one coherent explanation of what's likely driving the stock and what the models expect next. flag if the models meaningfully disagree with each other."""

	response= get_client().chat.completions.create(
		model="llama-3.3-70b-versatile",
		max_tokens=400,
		messages=[{"role":"user","content":prompt}],
	)
	summary= response.choices[0].message.content
	return {
		"symbol": symbol.upper(),
		"summary": summary,
		"last_close": ctx["last_close"],
		"predictions": ctx["predictions"],
		"top_features": ctx["top_features"],
	}