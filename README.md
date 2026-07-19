# StockUp

A stock analysis app. Live prices, price predictions from 4 different ML models with explanations for why, and a chat style Q&A that answers questions using real news and SEC filings.

## Features

- **Live prices** - real time price updates over WebSockets, plus basic indicators like RSI and moving averages
- **Predictions** - XGBoost, Random Forest, Linear Regression, and SVM all run together, shown side by side
- **Explainability** - SHAP shows exactly which factors pushed the prediction up or down
- **Ask why** - retrieves real news and SEC filings for a stock and answers questions using them, with sources
- **Full report** - one click summary combining live price, all 4 predictions, SHAP, and recent news into plain English

## Tech stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, WebSockets

**Machine learning:** XGBoost, scikit-learn, SHAP

**RAG:** Pinecone, Voyage AI, NewsAPI, SEC EDGAR, Groq (Llama 3.3 70B)

**Frontend:** React, Vite, Recharts

## Project structure

```
stockup/
|- backend/
|  |- main.py            starts the app, connects all routes
|  |- core/               settings, database connection
|  |- models/             database tables
|  |- data_service/        prices, search, live WebSocket
|  |- ml_service/          features, 4 models, SHAP
|  |- rag_service/         news/filings, embeddings, Q&A
|  |- agent_service/       combines everything into one report
|
|- frontend/
   |- src/
      |- App.jsx           layout, tabs, theme
      |- api.js             backend calls
      |- components/        ticker bar, search, theme toggle, loading screen
      |- components/tabs/   Chart, Predict, Ask, Report
```

## Running it locally

**Backend**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in your own keys
uvicorn main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## Deployment

Deployed on Render. 
PostgreSQL as a managed database, backend as a Web Service, frontend as a Static Site.
Free tier services sleep after inactivity, so the first request can take 30-60 seconds. 
The app shows a loading screen during that time.
