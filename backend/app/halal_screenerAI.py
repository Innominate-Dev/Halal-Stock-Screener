##from financial_model import train_financial_model, predict_financial
from app.nlp_model import load_nlp_model, predict_nlp, is_halal_business
import pandas as pd
import requests
import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    return{
        "business_summary": info.get("longBusinessSummary", ""),
        "sector": info.get("sector", ""),
        "debt": info.get("totalDebt", 0),
        "cash": info.get("totalCash", 0),
        "market_cap": info.get("marketCap", 1),  # prevent division by zero
        "receivables": info.get("totalReceivables", 0)
    }

def passes_financial_screening(data):
    try:
        market_cap = data['market_cap'] or 1
        debt_ratio = data['debt'] / market_cap
        cash_ratio = data['cash'] / market_cap
        receivable_ratio = data['recievables'] / market_cap

        is_compliant = (
            debt_ratio < 0.33 and
            cash_ratio < 0.33 and
            receivable_ratio <0.5
        )

        return {
            "debt_ratio": round(debt_ratio, 2),
            "cash_ratio": round(cash_ratio, 2),
            "receivable_ratio": round(receivable_ratio, 2),
            "is_shariah_compliant": is_compliant
        }
    except Exception as e:
        return {"error": str(e), "is_shariah_compliant": False}
    
def screen_stock(ticker):
    data = get_stock_data(ticker)
    business_status = is_halal_business(data["business_summary"])
    financial_status = passes_financial_screening(data)

    return{
        "ticker": ticker.upper(),
        "business_compliance": business_status,
        "financial_ratios": financial_status,
        "overall_halal":(
            business_status == "halal" and financial_status["is_shariah_compliant"]
        )
    }

# def get_financial_data(ticker):
#     # Example financial data: [debt_ratio, cash_ratio, receivables_ratio, interest_income_ratio]
#     return [[0.1, 0.05, 0.05, 0.01]]

# def get_company_description(ticker):
#     # Example company description: You can modify this or use dynamic fetching logic
#     return "We manufacture alcoholic beverages and provide financial services"

# def screen_stock(ticker, df):
#     """Screens a stock for halal/haram based on financials and NLP"""
    
#     # Load models
#     financial_model = train_financial_model(df)
#     nlp_pipeline = load_nlp_model()  # Fix typo here: from nlp_pipleline to nlp_pipeline

#     # Get data for the stock
#     financial_data = get_financial_data(ticker)
#     company_description = get_company_description(ticker)

#     # Predict using both models
#     financial_result = predict_financial(financial_model, financial_data)
#     nlp_result = predict_nlp(nlp_pipeline, company_description)

#     # Combine the results
#     # If any model is "Haram", mark as Haram
#     if financial_result[0] == "Haram" or nlp_result[0]['label'] == "Haram":
#         return f"Stock {ticker} is Haram"
    
#     # If either model is unsure, classify as Doubtful
#     if financial_result[0] == "Doubtful" or nlp_result[0]['label'] == "Doubtful":
#         return f"Stock {ticker} is Doubtful"
    
#     # If both models are confident Halal, classify as Halal
#     if financial_result[0] == "Halal" and nlp_result[0]['label'] == "Halal":
#         return f"Stock {ticker} is Halal"
    
#     return f"Stock {ticker} is Doubtful"  # Fallback to doubtful if no clear decision

# # Example usage
# if __name__ == "__main__":
#     # Sample data frame for financial model (replace with actual financial data)
#     df = pd.DataFrame({
#         'debt_ratio': [0.1, 0.4, 0.2, 0.3],
#         'cash_ratio': [0.05, 0.1, 0.2, 0.3],
#         'receivables_ratio': [0.05, 0.4, 0.1, 0.2],
#         'interest_income_ratio': [0.01, 0.07, 0.02, 0.03],
#         'label': ['Halal', 'Haram', 'Halal', 'Haram']
#     })

#     ticker = 'AAPL'  # Example ticker (Apple)
#     print(screen_stock(ticker, df))  # Output: Stock AAPL is Doubtful or another classification

#     ticker = 'TSLA'  # Tesla
#     print(screen_stock(ticker, df))  # Expected Output: Stock TSLA is Halal
    
#     ticker = 'SPWR'  # SunPower (solar energy company)
#     print(screen_stock(ticker, df))  # Expected Output: Stock SPWR is Halal

#     ticker = 'AIG'  # American International Group (Insurance)
#     print(screen_stock(ticker, df))  # Expected Output: Stock AIG is Haram





