# %% import libraries
import yfinance as yf
import pandas as pd
import numpy as np
from finvizfinance.screener.overview import Overview
import os
import time
import smtplib
from email.message import EmailMessage

# filters = ['exch_nasd', 'sec_technology', 'cap_mid', 'sh_avgvol_o1000']
filters_dict = {
    "Exchange": "NASDAQ",
    "Sector": "Technology",
    "Market Cap.": "Large ($10bln to $200bln)",
    "Average Volume": "Over 100K"
}
cache_file = "finviz_largecap_tech.csv"
max_cache_age_days = 7

# %% Check cache age
def is_cache_stale(path, max_age_days):
    if not os.path.exists(path):
        return True
    last_modified = os.path.getmtime(path)
    age_days = (time.time() - last_modified) / (60 * 60 * 24)
    return age_days > max_age_days

if is_cache_stale(cache_file, max_cache_age_days):
    overview = Overview()
    overview.set_filter(filters_dict=filters_dict)
    df_finviz = overview.screener_view()
    df_finviz.to_csv(cache_file, index=False)
else:
    df_finviz = pd.read_csv(cache_file)

# %% Extract tickers
tickers = df_finviz['Ticker'].tolist()

# %% Calculate growth scores

results = []
for ticker in tickers[:10]:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        market_cap = info.get("marketCap", np.nan)

        if not (2e9 <= market_cap <= 5e11):
            continue

        fin = stock.financials
        rev = fin.loc["Total Revenue"].dropna().sort_index()
        income_stmt = stock.income_stmt
        if "Net Income" not in income_stmt.index or len(rev) < 2 or len(income_stmt.loc["Net Income"].dropna()) < 2:
            continue

        net_income = income_stmt.loc["Net Income"].dropna().sort_index()
        revenue_growth = (rev.iloc[-1] - rev.iloc[-2]) / rev.iloc[-2]
        net_income_growth = (net_income.iloc[-1] - net_income.iloc[-2]) / net_income.iloc[-2]

        # Calculate 3-year CAGR for revenue and net income
        def cagr(series):
            n = len(series) - 1
            return (series.iloc[-1] / series.iloc[0]) ** (1/n) - 1 if n > 0 else np.nan

        rev_cagr = cagr(rev[-3:])
        net_income_cagr = cagr(net_income[-3:])

        results.append({
            "Ticker": ticker,
            "Market Cap ($B)": round(market_cap / 1e9, 2),
            "Revenue Growth YoY (%)": round(revenue_growth * 100, 2),
            "Net Income Growth YoY (%)": round(net_income_growth * 100, 2),
            "Rev CAGR": rev_cagr,
            "Net Income CAGR": net_income_cagr
        })

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

# Final DataFrame sorted by Growth Score
df = pd.DataFrame(results).sort_values(by="Rev CAGR", ascending=False)

# Normalize across all stocks after collecting results
df['Rev CAGR Z'] = (df['Rev CAGR'] - df['Rev CAGR'].mean()) / df['Rev CAGR'].std()
df['Net Income CAGR Z'] = (df['Net Income CAGR'] - df['Net Income CAGR'].mean()) / df['Net Income CAGR'].std()
df['Growth Score'] = 0.5 * df['Rev CAGR Z'] + 0.5 * df['Net Income CAGR Z']

df = df.sort_values(by="Growth Score", ascending=False)

top_df = df.head(5)

# Save or print
print(top_df)
# top_df.to_csv("mid_cap_tech_growth.csv", index=False)

#%% Send email with results via SMTP (HTML format)

def send_simple_message(subject, body_html):
    msg = EmailMessage()
    msg.set_content("This email contains an HTML table of the top 5 mid cap tech growth stocks.")  # Plain text fallback
    msg.add_alternative(body_html, subtype='html')
    msg["Subject"] = subject
    msg["From"] = "syuraj@gmail.com"
    msg["To"] = "syuraj@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("syuraj@gmail.com", os.getenv('GAPP_PWD'))
        smtp.send_message(msg)

if not top_df.empty:
    html_table = top_df.to_html(index=False, border=0)
    send_simple_message("Top 5 Mid Cap Tech Growth Stocks", html_table)
