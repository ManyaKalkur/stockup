from pinecone import Pinecone, ServerlessSpec
from core.config import settings

pc= Pinecone(api_key=settings.PINECONE_API_KEY)

def get_index():
	existing= [i.name for i in pc.list_indexes()]
	if settings.PINECONE_INDEX not in existing:
		pc.create_index(
			name=settings.PINECONE_INDEX,
			dimension=1024,  # voyage-2 embedding dim
			metric="cosine",
			spec=ServerlessSpec(cloud="aws",region="us-east-1"),
		)
	return pc.Index(settings.PINECONE_INDEX)