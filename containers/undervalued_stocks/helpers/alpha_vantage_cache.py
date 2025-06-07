import os
import time
import requests
import pandas as pd
import numpy as np

class AlphaVantageCache:
    def __init__(self, cache_dir="av_cache", cache_days=1, delay=2):
        self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("ALPHAVANTAGE_API_KEY environment variable not set.")
        self.cache_dir = cache_dir
        self.cache_days = cache_days
        self.delay = delay
        os.makedirs(cache_dir, exist_ok=True)

    def get_quarterly_income(self, ticker):
        return self._fetch_and_cache(ticker, "INCOME_STATEMENT", "income", "quarterlyReports")

    def get_quarterly_balance(self, ticker):
        return self._fetch_and_cache(ticker, "BALANCE_SHEET", "balance", "quarterlyReports")

    def get_quarterly_cashflow(self, ticker):
        return self._fetch_and_cache(ticker, "CASH_FLOW", "cashflow", "quarterlyReports")

    def get_overview_metrics(self, ticker):
        df = self._fetch_and_cache(ticker, "OVERVIEW", "overview", None)
        if not df.empty:
            row = df.iloc[0]
            return (
                float(row.get('PERatio', np.nan)),
                float(row.get('ProfitMargin', np.nan)),
                float(row.get('PEGRatio', np.nan)),
                float(row.get('ReturnOnEquityTTM', np.nan))
            )
        return np.nan, np.nan, np.nan, np.nan

    def _get_ticker_dir(self, ticker):
        ticker_dir = os.path.join(self.cache_dir, ticker)
        os.makedirs(ticker_dir, exist_ok=True)
        return ticker_dir

    def _get_cache_path(self, ticker, data_type):
        ticker_dir = self._get_ticker_dir(ticker)
        return os.path.join(ticker_dir, f"{data_type}.csv")

    def _is_cache_fresh(self, cache_path):
        if not os.path.exists(cache_path):
            return False
        age = time.time() - os.path.getmtime(cache_path)
        return age < self.cache_days * 86400

    def _fetch_and_cache(self, ticker, function, data_type, key):
        cache_path = self._get_cache_path(ticker, data_type)
        if self._is_cache_fresh(cache_path):
            return pd.read_csv(cache_path)
        time.sleep(self.delay)
        url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={self.api_key}"
        try:
            data = requests.get(url).json()
            if key is not None:
                df = pd.DataFrame(data.get(key, []))
            else:
                df = pd.DataFrame([data])
            df.to_csv(cache_path, index=False)
            return df
        except Exception as e:
            with open(os.path.join(self.cache_dir, "error.log"), "a") as f:
                f.write(f"Error fetching {function} for {ticker}: {e}\n")
            return pd.DataFrame()