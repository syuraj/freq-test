# %% import libraries
import yfinance as yf
import pandas as pd
import numpy as np
from finvizfinance.screener.overview import Overview
import os
import time
import importlib
import send_email
importlib.reload(send_email)
from send_email import send_styled_table_email

# Set pandas display options for better table formatting
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)

# Growth-focused filters
filters_dict = {
    "Sector": "Technology",
    "Market Cap.": "Large ($10bln to $200bln)",
    "IPO Date": "More than 5 years ago",

    # Growth indicators
    "EPS growththis year": "Positive (>0%)",
    "EPS growthnext year": "Positive (>0%)",
    "Sales growthqtr over qtr": "Positive (>0%)",
    "Sales growthpast 5 years": "Positive (>0%)",

    # Quality filters - LOOSENED
    "P/E": "Profitable (>0)",  # Keep this as it's important
    "Average Volume": "Over 50K",  # LOOSENED: Reduced from 50K to 10K
    "Return on Equity": "Positive (>0%)",  # LOOSENED: Reduced from >10% to just positive

    # Momentum indicators - LOOSENED
    # Removed "Performance": "Week Up" - too restrictive
    "Relative Volume": "Over 1",  # LOOSENED: Reduced from 1.5 to 1.0
}

cache_file = "finviz_largecap_growth.csv"
max_cache_age_days = 7
MIN_YEARS_REQUIRED = 2  # Minimal safety check

print(f"Targeting large cap growth companies...")
print(f"Using {len(filters_dict)} filters focused on growth")

# %% Check cache age
def is_cache_stale(path, max_age_days):
    if not os.path.exists(path):
        return True
    last_modified = os.path.getmtime(path)
    age_days = (time.time() - last_modified) / (60 * 60 * 24)
    return age_days > max_age_days

if is_cache_stale(cache_file, max_cache_age_days):
    print("Fetching fresh data from Finviz...")
    overview = Overview()
    overview.set_filter(filters_dict=filters_dict)
    df_finviz = overview.screener_view()

    if df_finviz is not None and not df_finviz.empty:
        df_finviz.to_csv(cache_file, index=False)
        print(f"Found {len(df_finviz)} growth companies")
    else:
        print("No companies found")
        exit()
else:
    print("Using cached data...")
    df_finviz = pd.read_csv(cache_file)
    print(f"Loaded {len(df_finviz)} companies from cache")

tickers = df_finviz['Ticker'].tolist()

# %% Calculate growth scores
def calculate_cagr(series, years=2):
    """Calculate CAGR for specified number of years"""
    if len(series) < years:
        return np.nan
    return (series.iloc[-1] / series.iloc[-years]) ** (1/(years-1)) - 1

results = []
print(f"\nAnalyzing {len(tickers)} growth companies...")

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        market_cap = info.get("marketCap", np.nan)

        fin = stock.financials
        income_stmt = stock.income_stmt

        if fin.empty or income_stmt.empty:
            continue

        if "Total Revenue" not in fin.index or "Net Income" not in income_stmt.index:
            continue

        rev = fin.loc["Total Revenue"].dropna().sort_index()
        net_income = income_stmt.loc["Net Income"].dropna().sort_index()

        if (len(rev) < MIN_YEARS_REQUIRED or len(net_income) < MIN_YEARS_REQUIRED):
            continue

        # Calculate growth metrics
        revenue_growth = (rev.iloc[-1] - rev.iloc[-2]) / rev.iloc[-2]
        net_income_growth = (net_income.iloc[-1] - net_income.iloc[-2]) / net_income.iloc[-2]
        rev_cagr = calculate_cagr(rev, MIN_YEARS_REQUIRED)
        net_income_cagr = calculate_cagr(net_income, MIN_YEARS_REQUIRED)

        if pd.isna(rev_cagr) or pd.isna(net_income_cagr):
            continue

        # Growth acceleration
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
            "Rev CAGR": round(rev_cagr * 100, 2),  # Convert to percentage
            "Net Income CAGR": round(net_income_cagr * 100, 2),  # Convert to percentage
            "Growth Acceleration": round(growth_acceleration * 100, 2),  # Convert to percentage
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

    # Growth-focused scoring (use original values for Z-score calculation)
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

    print(f"\n🚀 Analysis Complete:")
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
    if not top_df.empty:
        send_styled_table_email(
            "Top 5 Growth Stocks",
            display_df,
            "🏆 Top 5 Large Cap Tech Growth Companies"
        )

else:
    print("❌ No companies met the growth and data requirements")
    print("Consider expanding to more sectors or adjusting filters")
