# halal_screening.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

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

def fetch_company_profile(ticker):
    """Fetch company profile including sector and industry"""
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
    """Fetch key financial data: balance sheet and income statement latest"""
    # Balance Sheet
    bs_url = f"{FMP_BASE_URL}/balance-sheet-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"
    # Income Statement
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
    """
    Apply AAOIFI financial ratio rules:
    1) Debt/MarketCap <= 0.30
    2) InterestIncome/Revenue <= 0.05
    3) (Cash + ShortTermInvestments)/MarketCap <= 0.30
    """
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
    """
    Check if business sector or industry is haram based on keywords.
    """
    combined = f"{sector} {industry}".lower()
    for haram_sector in HARAM_SECTORS:
        if haram_sector.lower() in combined:
            return True, f"Business sector/industry contains haram activity: {haram_sector}"
    return False, ""

def check_ethical_issues(ticker):
    """
    Placeholder for ethical news/relations screening.
    This should be replaced with real news API calls or NGO databases.
    Returns (is_haram, reasons)
    """
    # TODO: implement real checks here
    # For now, assume no ethical issues
    return False, []

def screen_halal_stocks(ticker):
    try:
        profile = fetch_company_profile(ticker)
        financials = fetch_financial_statements(ticker)
        market_cap = profile.get("marketCap") or 0

        # 1) Business sector check
        haram_sector, sector_reason = check_business_sector(profile.get("sector", ""), profile.get("industry", ""))
        if haram_sector:
            return {
                "ticker": ticker,
                "status": "Haram ❌",
                "reason": sector_reason,
                "companyName": profile.get("companyName"),
            }

        # 2) AAOIFI financial ratio screening
        haram_financial, financial_reasons = apply_aaoifi_screening(financials, market_cap)
        if haram_financial:
            return {
                "ticker": ticker,
                "status": "Haram ❌",
                "reason": "; ".join(financial_reasons),
                "companyName": profile.get("companyName"),
            }

        # 3) Ethical/relations check (placeholder)
        haram_ethical, ethical_reasons = check_ethical_issues(ticker)
        if haram_ethical:
            return {
                "ticker": ticker,
                "status": "Haram ❌",
                "reason": "; ".join(ethical_reasons),
                "companyName": profile.get("companyName"),
            }

        # If none of the above checks failed:
        return {
            "ticker": ticker,
            "status": "Halal ✅",
            "reason": "Passed all AAOIFI financial and business sector checks.",
            "companyName": profile.get("companyName"),
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "status": "Error ⚠️",
            "reason": str(e),
            "companyName": None,
        }

def fetch_company_news(company_name):
    """Fetch recent news articles using NewsAPI.org"""
    news_api_key = os.getenv("NEWS_API_KEY")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company_name}&language=en&sortBy=publishedAt&pageSize=10&apiKey={news_api_key}"
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

def evaluate_ethical_risk(news_results, company_name):
    for article in news_results:
        if any(term in article["title"].lower() for term in ["israel", "settlement", "war crime", "weapons", "genocide", "oppression", "surveillance"]):
            return True, f"Flagged due to headline: {article['title']}"
        return False, "No red flags found."

if __name__ == "__main__":
    # Example tickers to test
    test_tickers = str(input("Input a ticketer: "))

    for tk in test_tickers:
        result = screen_halal_stocks(tk)
        print(f"{result['ticker']} ({result['companyName']}): {result['status']}")
        print(f"Reason: {result['reason']}")
        print("-" * 60)