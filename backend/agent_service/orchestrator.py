import anthropic
from core.config import settings
from data_service.prices import fetch_price_history
from ml_service.xgb_model import train_xgb
from ml_service.lstm_model import train_lstm
from ml_service.explain import explain_xgb
from rag_service.embed import embed_query
from rag_service.pinecone_client import get_index

client= anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def gather_context(symbol:str):
	rows= fetch_price_history(symbol,period="6mo")
	if len(rows)<60:
		return None
	xgb_result= train_xgb(rows)
	lstm_result= train_lstm(rows)
	explanation= explain_xgb(xgb_result["model"],xgb_result["features"]) if xgb_result else []
	index= get_index()
	q_emb= embed_query(f"recent news and events affecting {symbol} stock price")
	results= index.query(vector=q_emb,top_k=8,namespace=symbol.upper(),include_metadata=True)
	news_chunks= [m["metadata"]["text"] for m in results.get("matches",[])]
	return {
		"last_close": xgb_result["last_close"] if xgb_result else rows[-1]["close"],
		"xgb_prediction": xgb_result["prediction"] if xgb_result else None,
		"lstm_prediction": lstm_result["prediction"] if lstm_result else None,
		"top_features": explanation,
		"news_context": news_chunks,
	}

def generate_report(symbol:str):
	ctx= gather_context(symbol)
	if not ctx:
		return {"error":"not enough price history for this symbol"}

	news_block= "\n".join(f"- {c}" for c in ctx["news_context"]) or "no recent indexed news"
	features_block= ", ".join(f"{f['feature']} ({f['impact']})" for f in ctx["top_features"]) or "n/a"
	prompt= f"""write a short plain-english market brief for {symbol}. 3-4 sentences max, no headers.

last close: {ctx['last_close']}
xgboost next-day prediction: {ctx['xgb_prediction']}
lstm next-day prediction: {ctx['lstm_prediction']}
top price-driving features (shap): {features_block}

recent news context:
{news_block}

tie the technical signals and the news together into one coherent explanation of what's likely driving the stock and what the models expect next. flag if the two models disagree."""

	response= client.messages.create(
		model="claude-sonnet-4-6",
		max_tokens=400,
		messages=[{"role":"user","content":prompt}],
	)
	summary= "".join(b.text for b in response.content if b.type=="text")
	return {
		"symbol": symbol.upper(),
		"summary": summary,
		"last_close": ctx["last_close"],
		"xgb_prediction": ctx["xgb_prediction"],
		"lstm_prediction": ctx["lstm_prediction"],
		"top_features": ctx["top_features"],
	}