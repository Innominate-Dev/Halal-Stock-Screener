from sqlalchemy import create_engine, Column, String, Text, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import timezone, datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class HalalStock(Base):
    __tablename__ = "halal_stocks"
    
    ticker = Column(String, primary_key=True)
    company_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Float)
    status = Column(String)
    reason = Column(Text)
    financial_ratios = Column(JSON)
    news_flag = Column(String)
    news_snippet = Column(Text)
    last_updated = Column(DateTime, default=dt.now(timezone.utc))

def init_db():
    Base.metadata.create_all(engine)

def save_to_db(ticker, company_name, status, reason, sector, industry, market_cap, financial_ratios, news_flag, news_snippet):
    session = Session()
    if session.get(HalalStock, ticker) is None:
        stock = HalalStock(
            ticker=ticker,
            company_name=company_name,
            status=status,
            reason=reason,
            sector=sector,
            industry=industry,
            market_cap=market_cap,
            financial_ratios=financial_ratios,
            news_flag=news_flag,
            news_snippet=news_snippet,
            last_updated=dt.now(timezone.utc)
        )
        session.add(stock)
        session.commit()
    session.close()

def get_cached_stock(ticker):
    session = Session()
    stock = session.get(HalalStock, ticker)
    session.close()
    return stock

