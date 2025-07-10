from fastapi import FastAPI
from app.halal_screening import screen_halal_stocks
from app.db import init_db

app = FastAPI()
init_db()

@app.get("/")
def root():
    return {"message": "Halal Screener API"}

@app.get("/halal-stocks")
def get_halal_stocks():
    tickers = ["AAPL", "MSFT", "TSLA", "JPM", "KO", "NVDA", "META", "MKDW"]
    results = screen_halal_stocks(tickers)
    return{"halal": results}