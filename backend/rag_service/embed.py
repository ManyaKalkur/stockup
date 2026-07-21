import voyageai
from core.config import settings

_client= None
def get_client():
    global _client
    if _client is None:
        _client= voyageai.Client(api_key=settings.VOYAGE_API_KEY)
    return _client

def embed_texts(texts: list, input_type="document"):
    client= get_client()
    result= client.embed(
        texts,
        model="voyage-2",
        input_type=input_type,
    )
    return result.embeddings

def embed_query(text: str):
    return embed_texts([text], input_type="query")[0]