from finviz_screener import FinvizScreener

# Initialize screener
screener = FinvizScreener(cache_days=7)

# Example 1: Growth Tech Stocks
print("🚀 GROWTH TECH SCREENING")
print("=" * 30)
growth_filters = screener.get_growth_tech_filters()
growth_stocks = screener.screen_stocks(growth_filters, "growth_tech")
growth_tickers = screener.get_tickers_list(growth_stocks)
print(f"Found {len(growth_tickers)} growth tech stocks")
print("Top 10:", growth_tickers[:10])

# Example 2: Value Stocks
print("\n💰 VALUE SCREENING")
print("=" * 20)
value_filters = screener.get_value_filters()
value_stocks = screener.screen_stocks(value_filters, "value_stocks")
value_tickers = screener.get_tickers_list(value_stocks)
print(f"Found {len(value_tickers)} value stocks")
print("Top 10:", value_tickers[:10])

# Example 3: Momentum Stocks
print("\n📈 MOMENTUM SCREENING")
print("=" * 25)
momentum_filters = screener.get_momentum_filters()
momentum_stocks = screener.screen_stocks(momentum_filters, "momentum_stocks")
momentum_tickers = screener.get_tickers_list(momentum_stocks)
print(f"Found {len(momentum_tickers)} momentum stocks")
print("Top 10:", momentum_tickers[:10])

# Example 4: Custom Filter
print("\n🎯 CUSTOM SCREENING")
print("=" * 22)
custom_filters = {
    "Sector": "Healthcare",
    "Market Cap.": "+Large (over $10bln)",
    "P/E": "Low (<20)",
    "ROE": "High (>10%)",
    "Debt/Eq": "Low (<0.5)"
}
custom_stocks = screener.screen_stocks(custom_filters, "healthcare_quality")
custom_tickers = screener.get_tickers_list(custom_stocks)
print(f"Found {len(custom_tickers)} healthcare quality stocks")
print("Top 10:", custom_tickers[:10])

# Summary statistics
print("\n📊 SUMMARY STATS")
print("=" * 18)
for name, df in [("Growth", growth_stocks), ("Value", value_stocks),
                 ("Momentum", momentum_stocks), ("Custom", custom_stocks)]:
    stats = screener.summary_stats(df)
    print(f"{name}: {stats.get('total_companies', 0)} companies")