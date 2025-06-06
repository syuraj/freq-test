# %% import libraries
import yfinance as yf
import pandas as pd
import numpy as np
import os
import time
import importlib
import send_email
importlib.reload(send_email)
from send_email import send_styled_table_email
import yahoo_finance_cache
importlib.reload(yahoo_finance_cache)
from yahoo_finance_cache import YahooFinanceCache
from finviz_screener import FinvizScreener

# Set pandas display options for better table formatting
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)

# Initialize screeners
yf_cache = YahooFinanceCache(
    cache_days=1,           # Cache for 1 day
    rate_limit_delay=1.0    # 1 second delay between calls
)

finviz_screener = FinvizScreener(
    cache_days=7
)

# Minimum number of quarters required (8 quarters = 2 years)
MIN_PERIODS_REQUIRED = 8

print(f"Targeting large cap growth companies...")

# %% Get Finviz data
filters_dict = finviz_screener.get_growth_tech_filters()
print(f"Using {len(filters_dict)} Finviz filters focused on growth")

df_finviz = finviz_screener.screen_stocks(
    filters_dict=filters_dict,
    screen_name="largecap_growth"
)

if df_finviz.empty:
    print("No companies found")
    exit()

tickers = finviz_screener.get_tickers_list(df_finviz)
print(f"Selected {len(tickers)} companies for analysis")

# %% Calculate growth scores
def calculate_cqgr(series, periods=8):
    """Calculate Compound Quarterly Growth Rate (CQGR) for specified number of periods (quarters)"""
    if len(series) < periods:
        return np.nan
    return (series.iloc[-1] / series.iloc[-periods]) ** (1/(periods-1)) - 1

results = []

print(f"\nAnalyzing {len(tickers)} growth companies...")
print(f"API rate limit: {yf_cache.rate_limit_delay}s between calls")

for ticker in tickers[:2]:
    try:
        print(f"Processing {ticker}...")
        stock_data = yf_cache.get_data(ticker)
        if stock_data is None:
            continue

        info = stock_data['info']
        fin = stock_data['quarterly_financials']
        income_stmt = stock_data['quarterly_income_stmt']

        market_cap = info.get("marketCap", np.nan)

        if fin.empty or income_stmt.empty:
            continue

        if "Total Revenue" not in fin.index or "Net Income" not in income_stmt.index:
            continue

        rev = fin.loc["Total Revenue"].dropna().sort_index()
        net_income = income_stmt.loc["Net Income"].dropna().sort_index()

        if (len(rev) < MIN_PERIODS_REQUIRED or len(net_income) < MIN_PERIODS_REQUIRED):
            continue

        revenue_growth = (rev.iloc[-1] - rev.iloc[-2]) / rev.iloc[-2]
        net_income_growth = (net_income.iloc[-1] - net_income.iloc[-2]) / net_income.iloc[-2]
        rev_cagr = calculate_cqgr(rev, MIN_PERIODS_REQUIRED)
        net_income_cagr = calculate_cqgr(net_income, MIN_PERIODS_REQUIRED)

        if pd.isna(rev_cagr) or pd.isna(net_income_cagr):
            continue

        if len(rev) >= 4 and rev.iloc[-3] != 0:
            prev_growth = (rev.iloc[-2] - rev.iloc[-3]) / rev.iloc[-3]
            growth_acceleration = revenue_growth - prev_growth
        else:
            growth_acceleration = 0

        results.append({
            "Ticker": ticker,
            "Market Cap ($B)": round(market_cap / 1e9, 2),
            "Revenue Growth YoY (%)": round(revenue_growth * 100, 2),
            "Net Income Growth YoY (%)": round(net_income_growth * 100, 2),
            "Rev CAGR": round(rev_cagr * 100, 2),
            "Net Income CAGR": round(net_income_cagr * 100, 2),
            "Growth Acceleration": round(growth_acceleration * 100, 2),
        })

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

# %% Scoring
if results:
    df = pd.DataFrame(results)

    def safe_zscore(series):
        if series.std() == 0:
            return pd.Series([0] * len(series), index=series.index)
        return (series - series.mean()) / series.std()

    # Growth-focused scoring
    df['Rev CAGR Z'] = safe_zscore(df['Rev CAGR'])
    df['Net Income CAGR Z'] = safe_zscore(df['Net Income CAGR'])
    df['Recent Rev Growth Z'] = safe_zscore(df['Revenue Growth YoY (%)'])
    df['Growth Accel Z'] = safe_zscore(df['Growth Acceleration'])

    # Combined score
    df['Growth Score'] = (
        0.3 * df['Rev CAGR Z'] +
        0.2 * df['Net Income CAGR Z'] +
        0.3 * df['Recent Rev Growth Z'] +
        0.2 * df['Growth Accel Z']
    )

    df = df.sort_values(by="Growth Score", ascending=False)
    top_df = df.head(5)

    print(f"\nAnalysis Complete:")
    print(f"✅ Successfully analyzed {len(df)} companies")
    print(f"📊 Filter efficiency: {len(df)}/{len(tickers)} = {len(df)/len(tickers)*100:.1f}%")

    display_df = top_df[['Ticker', 'Market Cap ($B)', 'Revenue Growth YoY (%)',
                        'Net Income Growth YoY (%)', 'Rev CAGR', 'Net Income CAGR', 'Growth Score']].copy()

    # Round Growth Score for display
    display_df['Growth Score'] = display_df['Growth Score'].round(2)

    print("\n🏆 TOP 5 GROWTH COMPANIES")
    print("=" * 26)
    print(display_df)

    # Send styled email
    # if not top_df.empty:
    #     send_styled_table_email(
    #         "Top 5 Growth Stocks",
    #         display_df,
    #         "🏆 Top 5 Large Cap Tech Growth Companies"
    #     )

else:
    print("❌ No companies met the growth and data requirements")
    print("Consider expanding to more sectors or adjusting filters")
