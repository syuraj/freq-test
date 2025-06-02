import yfinance as yf
import pandas as pd
import os
from datetime import datetime

class YahooFinanceCache:
    def __init__(self, cache_dir="yf_cache", cache_days=1):
        self.cache_dir = cache_dir
        self.cache_days = cache_days
        os.makedirs(cache_dir, exist_ok=True)

    def _get_ticker_dir(self, ticker):
        return os.path.join(self.cache_dir, ticker)

    def _is_cache_fresh(self, ticker):
        timestamp_file = os.path.join(self._get_ticker_dir(ticker), 'timestamp.txt')
        if not os.path.exists(timestamp_file):
            return False

        with open(timestamp_file, 'r') as f:
            cache_time = float(f.read())

        return datetime.now().timestamp() - cache_time <= (self.cache_days * 24 * 60 * 60)

    def save_data(self, ticker, stock_data):
        ticker_dir = self._get_ticker_dir(ticker)
        os.makedirs(ticker_dir, exist_ok=True)

        if 'info' in stock_data and stock_data['info']:
            info_df = pd.DataFrame([stock_data['info']])
            info_df.to_csv(os.path.join(ticker_dir, 'info.csv'), index=False)

        for data_type in ['financials', 'income_stmt', 'balance_sheet', 'cashflow']:
            if data_type in stock_data and not stock_data[data_type].empty:
                stock_data[data_type].to_csv(os.path.join(ticker_dir, f'{data_type}.csv'))

        with open(os.path.join(ticker_dir, 'timestamp.txt'), 'w') as f:
            f.write(str(datetime.now().timestamp()))

    def load_data(self, ticker):
        if not self._is_cache_fresh(ticker):
            return None

        ticker_dir = self._get_ticker_dir(ticker)
        stock_data = {}

        info_file = os.path.join(ticker_dir, 'info.csv')
        if os.path.exists(info_file):
            info_df = pd.read_csv(info_file)
            stock_data['info'] = info_df.iloc[0].to_dict() if not info_df.empty else {}

        for data_type in ['financials', 'income_stmt', 'balance_sheet', 'cashflow']:
            file_path = os.path.join(ticker_dir, f'{data_type}.csv')
            if os.path.exists(file_path):
                stock_data[data_type] = pd.read_csv(file_path, index_col=0)
            else:
                stock_data[data_type] = pd.DataFrame()

        return stock_data

    def get_data(self, ticker):
        cached_data = self.load_data(ticker)
        if cached_data is not None:
            print(f"Loading {ticker} from cache...")
            return cached_data

        print(f"Fetching {ticker} from Yahoo Finance...")
        try:
            stock = yf.Ticker(ticker)
            stock_data = {
                'info': stock.info,
                'financials': stock.financials,
                'income_stmt': stock.income_stmt,
                'balance_sheet': stock.balance_sheet,
                'cashflow': stock.cashflow
            }
            self.save_data(ticker, stock_data)
            return stock_data
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None