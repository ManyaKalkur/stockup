from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import Base, engine
from data_service.router import router as data_router
from ml_service.router import router as ml_router
from rag_service.router import router as rag_router
from agent_service.router import router as agent_router

app= FastAPI(title="StockUp", description="StockUp is a platform that provides stock market data, machine learning insights, and retrieval-augmented generation capabilities for financial analysis.")
app.include_router(data_router,prefix="/api/data")
app.include_router(ml_router,prefix="/api/ml")
app.include_router(rag_router,prefix="/api/rag")
app.include_router(agent_router,prefix="/api/agent")

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.CORS_ORIGINS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.on_event("startup")
def startup():
	Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
	return {"status":"ok"}