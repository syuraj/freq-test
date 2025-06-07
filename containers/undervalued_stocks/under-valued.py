# %% import libraries
import pandas as pd
import numpy as np
import os
import time
import importlib
import send_email
importlib.reload(send_email)
from send_email import send_styled_table_email
from alpha_vantage_cache import AlphaVantageCache
from finviz_screener import FinvizScreener

# Set pandas display options for better table formatting
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)

av_cache = AlphaVantageCache(
    cache_days=1           # Cache for 1 day
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
    """Calculate Compound Quarterly Growth Rate (CQGR) for the last 8 periods/quarters, assuming chronological order (oldest to newest)."""
    if len(series) < periods:
        return np.nan
    s = series.iloc[-periods:]
    if s.iloc[0] <= 0 or s.iloc[-1] <= 0:
        return np.nan
    return (s.iloc[-1] / s.iloc[0]) ** (1/(periods-1)) - 1

results = []

print(f"\nAnalyzing {len(tickers)} growth companies...")
for ticker in tickers[:3]:
    try:
        print(f"Processing {ticker}...")
        income_df = av_cache.get_quarterly_income(ticker)

        rev = pd.to_numeric(
            income_df.set_index('fiscalDateEnding')['totalRevenue'], errors='coerce'
        ).dropna().sort_index()
        net_income = pd.to_numeric(
            income_df.set_index('fiscalDateEnding')['netIncome'], errors='coerce'
        ).dropna().sort_index()
        if (len(rev) < MIN_PERIODS_REQUIRED or len(net_income) < MIN_PERIODS_REQUIRED):
            continue
        revenue_growth = (rev.iloc[0] - rev.iloc[1]) / rev.iloc[1]
        net_income_growth = (net_income.iloc[0] - net_income.iloc[1]) / net_income.iloc[1]
        rev_cagr = calculate_cqgr(rev, MIN_PERIODS_REQUIRED)
        net_income_cagr = calculate_cqgr(net_income, MIN_PERIODS_REQUIRED)
        if pd.isna(rev_cagr) or pd.isna(net_income_cagr):
            continue
        if len(rev) >= 4 and rev.iloc[2] != 0:
            prev_growth = (rev.iloc[1] - rev.iloc[2]) / rev.iloc[2]
            growth_acceleration = revenue_growth - prev_growth
        else:
            growth_acceleration = 0

        pe, profit_margin, peg, roe = av_cache.get_overview_metrics(ticker)
        results.append({
            "Ticker": ticker,
            "Revenue Growth QoQ (%)": round(revenue_growth * 100, 2),
            "Net Income Growth QoQ (%)": round(net_income_growth * 100, 2),
            "Rev CAGR": round(rev_cagr * 100, 2),
            "Net Income CAGR": round(net_income_cagr * 100, 2),
            "Growth Acceleration": round(growth_acceleration * 100, 2),
            "P/E Ratio": pe,
            "Profit Margin": profit_margin,
            "PEG Ratio": peg,
            "ROE": roe,
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
    df['Recent Rev Growth Z'] = safe_zscore(df['Revenue Growth QoQ (%)'])
    df['Growth Accel Z'] = safe_zscore(df['Growth Acceleration'])
    # Z-scores for overview metrics (across all stocks)
    df['P/E Z'] = safe_zscore(df['P/E Ratio'])
    df['Cheapness Z'] = -df['P/E Z']  # Lower P/E is better
    df['Profit Margin Z'] = safe_zscore(df['Profit Margin'])
    df['PEG Z'] = -safe_zscore(df['PEG Ratio'])  # Lower PEG is better
    df['ROE Z'] = safe_zscore(df['ROE'])  # Higher ROE is better

    # Combined growth-only score
    df['Growth Score'] = (
        0.3 * df['Rev CAGR Z'] +
        0.2 * df['Net Income CAGR Z'] +
        0.3 * df['Recent Rev Growth Z'] +
        0.2 * df['Growth Accel Z']
    )
    # Composite score: growth + value + quality
    df['Composite Score'] = (
        0.13 * df['Rev CAGR Z'] +
        0.12 * df['Net Income CAGR Z'] +
        0.13 * df['Recent Rev Growth Z'] +
        0.12 * df['Growth Accel Z'] +
        0.13 * df['Cheapness Z'] +
        0.10 * df['Profit Margin Z'] +
        0.13 * df['PEG Z'] +
        0.14 * df['ROE Z']
    )

    df = df.sort_values(by="Composite Score", ascending=False)
    top_df = df.head(5)

    print(f"\nAnalysis Complete:")
    print(f"✅ Successfully analyzed {len(df)} companies")
    print(f"📊 Filter efficiency: {len(df)}/{len(tickers)} = {len(df)/len(tickers)*100:.1f}%")

    display_df = top_df[['Ticker', 'Revenue Growth QoQ (%)',
                        'Net Income Growth QoQ (%)', 'Rev CAGR', 'Net Income CAGR', 'Growth Score', 'Composite Score']].copy()

    display_df['Growth Score'] = display_df['Growth Score'].round(2)
    display_df['Composite Score'] = display_df['Composite Score'].round(2)

    print("\n🏆 TOP 5 GROWTH + VALUE COMPANIES")
    print("=" * 34)
    print(display_df)

    if not top_df.empty:
        send_styled_table_email(
            "Top 5 Growth + Value Stocks",
            display_df,
            "🏆 Top 5 Large Cap Tech Growth + Value Companies"
        )

else:
    print("❌ No companies met the growth and data requirements")
    print("Consider expanding to more sectors or adjusting filters")

