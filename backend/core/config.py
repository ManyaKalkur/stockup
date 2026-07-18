import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
	DATABASE_URL= os.getenv("DATABASE_URL","postgresql://localhost/stockrag")
	REDIS_URL= os.getenv("REDIS_URL","redis://localhost:6379")
	ANTHROPIC_API_KEY= os.getenv("ANTHROPIC_API_KEY")
	NEWSAPI_KEY= os.getenv("NEWSAPI_KEY")
	PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
	PINECONE_INDEX= os.getenv("PINECONE_INDEX","stock-rag")
	VOYAGE_API_KEY= os.getenv("VOYAGE_API_KEY")
	SEC_EDGAR_USER_AGENT= os.getenv("SEC_EDGAR_USER_AGENT","stockrag-app contact@example.com")
	CORS_ORIGINS= os.getenv("CORS_ORIGINS","http://localhost:5173,https://stockup-2f05.onrender.com").split(",")
settings= Settings()