"""
Systematic screening of undervalued, high-growth, innovative US technology stocks.

- Universe: Large/Mid-cap US tech stocks (example tickers, expand as needed)
- Valuation: P/E, PEG, EV/EBITDA
- Growth: YoY revenue growth, R&D as % of revenue
- Innovation: Placeholder for patent/product data (see USPTO/Google Patents APIs)

Dependencies:
    pip install yfinance pandas

Author: Roo
"""

import yfinance as yf
import pandas as pd

# Example universe: expand with more tickers or automate with screener APIs
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "META", "NVDA", "ADBE", "CRM", "INTC", "AMD", "CSCO"
]

yf.set_config(requests_backend="requests")

def get_financial_metrics(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # Valuation
    pe = info.get("trailingPE")
    peg = info.get("pegRatio")
    ev_to_ebitda = info.get("enterpriseToEbitda")
    market_cap = info.get("marketCap")
    sector = info.get("sector")

    # Growth
    try:
        fin = stock.financials
        revenue = fin.loc["Total Revenue"].iloc[0]
        prev_revenue = fin.loc["Total Revenue"].iloc[1]
        yoy_growth = (revenue - prev_revenue) / prev_revenue * 100
        r_and_d = fin.loc["Research Development"].iloc[0]
        r_and_d_pct = r_and_d / revenue * 100
    except Exception:
        yoy_growth = None
        r_and_d_pct = None

    # Innovation (placeholder)
    patent_count = None  # Integrate with USPTO/Google Patents API

    return {
        "Ticker": ticker,
        "P/E": pe,
        "PEG": peg,
        "EV/EBITDA": ev_to_ebitda,
        "Market Cap": market_cap,
        "Sector": sector,
        "YoY Growth %": yoy_growth,
        "R&D %": r_and_d_pct,
        "Patent Count": patent_count
    }

def screen_stocks(tickers):
    results = []
    for ticker in tickers:
        metrics = get_financial_metrics(ticker)
        # Screening criteria
        if (
            metrics["Sector"] == "Technology"
            and metrics["Market Cap"] and metrics["Market Cap"] > 10_000_000_000
            and metrics["P/E"] and metrics["P/E"] < 25
            and metrics["PEG"] and metrics["PEG"] < 1.5
            and metrics["EV/EBITDA"] and metrics["EV/EBITDA"] < 15
            and metrics["YoY Growth %"] and metrics["YoY Growth %"] > 10
            and metrics["R&D %"] and metrics["R&D %"] > 5
        ):
            results.append(metrics)
    return pd.DataFrame(results)

if __name__ == "__main__":
    df = screen_stocks(TICKERS)
    df = df.sort_values(by="YoY Growth %", ascending=False)
    print("Screened US Tech Stocks (Undervalued, High Growth, Innovative):")
    print(df)
    df.to_csv("screened_tech_stocks.csv", index=False)
    print("\nResults saved to screened_tech_stocks.csv")

# For innovation data, see:
# - USPTO Patent API: https://developer.uspto.gov/
# - Google Patents Public Datasets: https://console.cloud.google.com/marketplace/product/google_patents_public_datasets

print(yf.Ticker("AAPL").info)