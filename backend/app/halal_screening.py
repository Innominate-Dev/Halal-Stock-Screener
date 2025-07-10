# halal_screening.py
import requests
import os
from dotenv import load_dotenv
from app.db import init_db, save_to_db, get_cached_stock

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# --- Define haram sectors to exclude ---
HARAM_SECTORS = [
    "Gambling",
    "Alcohol",
    "Tobacco",
    "Adult Entertainment",
    "Conventional Banking",
    "Insurance",
    "Military Hardware",
    "Defense",
    "Weapons",
]

DOUBTFUL_TERMS = [
    "accused of", "linked to", "criticism", "controversy", "allegations", "boycott",
    "may be involved", "under investigation", "reportedly", "activists"
]

CLEAR_HARAM_TERMS = [
    "war crimes", "genocide", "weapons", "arms sales", "surveillance", "oppression",
    "settlement support", "illegal occupation", "military contracts"
]

def fetch_company_profile(ticker):
    url = f"{FMP_BASE_URL}/profile/{ticker}?apikey={FMP_API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200 or not resp.json():
        raise ValueError(f"Could not fetch profile for {ticker}")
    data = resp.json()[0]
    return {
        "companyName": data.get("companyName"),
        "sector": data.get("sector"),
        "industry": data.get("industry"),
        "marketCap": data.get("mktCap"),
        "beta": data.get("beta"),
    }

def fetch_financial_statements(ticker):
    bs_url = f"{FMP_BASE_URL}/balance-sheet-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"
    inc_url = f"{FMP_BASE_URL}/income-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"

    bs_resp = requests.get(bs_url)
    inc_resp = requests.get(inc_url)

    if bs_resp.status_code != 200 or inc_resp.status_code != 200:
        raise ValueError(f"Could not fetch financials for {ticker}")

    bs_data = bs_resp.json()
    inc_data = inc_resp.json()
    if not bs_data or not inc_data:
        raise ValueError(f"Financial data missing for {ticker}")

    bs = bs_data[0]
    inc = inc_data[0]

    return {
        "totalDebt": bs.get("totalDebt", 0),
        "cashAndCashEquivalents": bs.get("cashAndCashEquivalents", 0),
        "shortTermInvestments": bs.get("shortTermInvestments", 0),
        "interestIncome": inc.get("interestIncome", 0),
        "totalRevenue": inc.get("revenue", 0),
    }

def apply_aaoifi_screening(financials, market_cap):
    reasons = []
    is_haram = False

    debt_ratio = financials["totalDebt"] / market_cap if market_cap else 0
    if debt_ratio > 0.3:
        reasons.append(f"Debt/MarketCap ratio too high: {debt_ratio:.2f} > 0.30")
        is_haram = True

    interest_ratio = financials["interestIncome"] / financials["totalRevenue"] if financials["totalRevenue"] else 0
    if interest_ratio > 0.05:
        reasons.append(f"Interest income/Revenue ratio too high: {interest_ratio:.2f} > 0.05")
        is_haram = True

    cash_ratio = (financials["cashAndCashEquivalents"] + financials["shortTermInvestments"]) / market_cap if market_cap else 0
    if cash_ratio > 0.3:
        reasons.append(f"Cash + short-term investments/MarketCap ratio too high: {cash_ratio:.2f} > 0.30")
        is_haram = True

    return is_haram, reasons

def check_business_sector(sector, industry):
    combined = f"{sector} {industry}".lower()
    for haram_sector in HARAM_SECTORS:
        if haram_sector.lower() in combined:
            return True, f"Business sector/industry contains haram activity: {haram_sector}"
    return False, ""

def fetch_company_news(company_name):
    url = (
        f"https://newsapi.org/v2/everything?q={company_name}&language=en"
        f"&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"News API error: {response.status_code}")
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        print(f"[ERROR] News fetch failed for {company_name}: {e}")
        return []

def evaluate_ethical_risk(news_articles):
    haram_flags = []
    doubtful_flags = []

    for article in news_articles:
        title = article.get("title", "").lower()
        if any(term in title for term in CLEAR_HARAM_TERMS):
            haram_flags.append(title)
        elif any(term in title for term in DOUBTFUL_TERMS):
            doubtful_flags.append(title)

    if haram_flags:
        return "Haram ❌", f"Flagged due to article(s): {haram_flags[0]}"
    elif doubtful_flags:
        return "Doubtful ⚠️", f"Unclear concerns found, e.g.: {doubtful_flags[0]} — human verification suggested."
    else:
        return "Halal ✅", "No concerning news found."

def screen_halal_stocks(ticker):
    try:
        # Early exit if stock is already screened
        cached = get_cached_stock(ticker)
        if cached:
            return {
                "ticker": cached.ticker,
                "status": cached.status,
                "reason": cached.reason,
                "companyName": cached.company_name,
            }
        profile = fetch_company_profile(ticker)
        financials = fetch_financial_statements(ticker)
        market_cap = profile.get("marketCap") or 0

        haram_sector, sector_reason = check_business_sector(profile.get("sector", ""), profile.get("industry", ""))
        if haram_sector:
            return {
                "ticker": ticker,
                "status": "Haram ❌",
                "reason": sector_reason,
                "companyName": profile.get("companyName"),
            }

        haram_financial, financial_reasons = apply_aaoifi_screening(financials, market_cap)
        if haram_financial:
            return {
                "ticker": ticker,
                "status": "Haram ❌",
                "reason": "; ".join(financial_reasons),
                "companyName": profile.get("companyName"),
            }

        news_results = fetch_company_news(profile.get("companyName"))
        ethical_status, ethical_reason = evaluate_ethical_risk(news_results)

        return {
            "ticker": ticker,
            "status": ethical_status,
            "reason": ethical_reason,
            "companyName": profile.get("companyName"),
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "status": "Error ⚠️",
            "reason": str(e),
            "companyName": None,
        }

if __name__ == "__main__":
    test_tickers = input("Enter a ticker: ").split()
    print(test_tickers)
    
    for tk in test_tickers:
        result = screen_halal_stocks(tk)
        save_to_db(result["ticker"], result["companyName"], result["status"], result["reason"])
        
        print(f"{result['ticker']} ({result['companyName']}): {result['status']}")
        print(f"Reason: {result['reason']}")
        print("-" * 60)
