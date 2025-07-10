import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class HalalStock(Base):
    __tablename__ = "halal_stocks"
    
    ticker = Column(String,primary_key=True)
    company_name = Column(String)
    status = Column(String)
    reason = Column(Text)

def init_db():
    Base.metadata.create_all(engine)

def save_to_db(ticker, company_name, status, reason):
    session = Session()
    if session.get(HalalStock, ticker) is None:
        stock = HalalStock(
            ticker=ticker,
            company_name=company_name,
            status=status,
            reason=reason
        )
        session.add(stock)
        session.commit()
    session.close()

def get_cached_stock(ticker):
    session = Session()
    stock = session.get(HalalStock, ticker)
    session.close()
    return stock

