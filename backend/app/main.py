from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.halal_screening import screen_halal_stocks, screen_halal_stocks_batch
from app.db import init_db
from app.halal_screenerAI import screen_stock

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Halal Screener API"}

@app.get("/screen/{ticker}")
def screen_endpoint(ticker: str):
    result = screen_stock(ticker)
    return result

@app.get("/stocks")
def get_stock(ticker: str=Query(..., min_length=1)):
    return screen_halal_stocks(ticker)

@app.get("/stocks-screener")
def get_halal_stocks_batch():
    tickers = ["AAPL", "MSFT", "TSLA", "JPM", "KO", "NVDA", "META", "MKDW"]
    return screen_halal_stocks_batch(tickers)

@app.get("/health")
def health_check():
    return {"status": "ok"}