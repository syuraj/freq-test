import pandas as pd
import os
import time
from finvizfinance.screener.overview import Overview

class FinvizScreener:
    def __init__(self, cache_dir="finviz_cache", cache_days=7):
        self.cache_dir = cache_dir
        self.cache_days = cache_days
        os.makedirs(cache_dir, exist_ok=True)

    def _is_cache_stale(self, cache_file, max_age_days):
        if not os.path.exists(cache_file):
            return True
        last_modified = os.path.getmtime(cache_file)
        age_days = (time.time() - last_modified) / (60 * 60 * 24)
        return age_days > max_age_days

    def _get_cache_file_path(self, screen_name):
        return os.path.join(self.cache_dir, f"{screen_name}.csv")

    def screen_stocks(self, filters_dict, screen_name="default_screen"):
        cache_file = self._get_cache_file_path(screen_name)

        if self._is_cache_stale(cache_file, self.cache_days):
            print(f"Fetching fresh data from Finviz for {screen_name}...")
            overview = Overview()
            overview.set_filter(filters_dict=filters_dict)
            df_finviz = overview.screener_view()

            if df_finviz is not None and not df_finviz.empty:
                df_finviz.to_csv(cache_file, index=False)
                print(f"Found {len(df_finviz)} companies matching criteria")
                return df_finviz
            else:
                print("No companies found matching criteria")
                return pd.DataFrame()
        else:
            print(f"Using cached Finviz data for {screen_name}...")
            df_finviz = pd.read_csv(cache_file)
            print(f"Loaded {len(df_finviz)} companies from cache")
            return df_finviz

    def get_growth_tech_filters(self):
        """Predefined filters for large-cap tech growth companies"""
        return {
            "Sector": "Technology",
            "Market Cap.": "Large ($10bln to $200bln)",
            "IPO Date": "More than 5 years ago",
            "EPS growththis year": "Positive (>0%)",
            "EPS growthnext year": "Positive (>0%)",
            "Sales growthqtr over qtr": "Positive (>0%)",
            "Sales growthpast 5 years": "Positive (>0%)",
            "P/E": "Profitable (>0)",
            "Average Volume": "Over 50K",
            "Return on Equity": "Positive (>0%)",
            "Relative Volume": "Over 1",
        }

    def get_value_filters(self):
        """Predefined filters for value investing"""
        return {
            "P/E": "Low (<15)",
            "P/B": "Low (<3)",
            "P/S": "Low (<3)",
            "PEG": "Low (<1)",
            "Debt/Eq": "Low (<0.5)",
            "ROE": "High (>15%)",
            "ROI": "High (>10%)",
            "Market Cap.": "+Large (over $10bln)",
        }

    def get_momentum_filters(self):
        """Predefined filters for momentum investing"""
        return {
            "Performance (Week)": "Up",
            "Performance (Month)": "Up",
            "Performance (Quarter)": "Up",
            "Relative Volume": "Over 1.5",
            "Average Volume": "Over 100K",
            "Price": "Over $5",
            "Market Cap.": "+Mid (over $2bln)",
        }

    def get_tickers_list(self, df_finviz):
        """Extract ticker list from Finviz DataFrame"""
        if df_finviz.empty:
            return []
        return df_finviz['Ticker'].tolist()

    def summary_stats(self, df_finviz):
        """Get summary statistics of the screened companies"""
        if df_finviz.empty:
            return {}

        stats = {
            "total_companies": len(df_finviz),
            "sectors": df_finviz['Sector'].value_counts().to_dict() if 'Sector' in df_finviz.columns else {},
            "avg_market_cap": df_finviz['Market Cap'].mean() if 'Market Cap' in df_finviz.columns else None,
            "industries": df_finviz['Industry'].value_counts().head(5).to_dict() if 'Industry' in df_finviz.columns else {}
        }
        return stats