import voyageai
from core.config import settings

vo= voyageai.Client(api_key=settings.VOYAGE_API_KEY)

def embed_texts(texts:list, input_type="document"):
	result= vo.embed(texts,model="voyage-2",input_type=input_type)
	return result.embeddings

def embed_query(text:str):
	return embed_texts([text],input_type="query")[0]