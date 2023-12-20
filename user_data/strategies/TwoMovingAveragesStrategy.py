from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, stoploss_from_open, DecimalParameter,
                                IntParameter, IStrategy, informative, merge_informative_pair)

class TwoMovingAveragesStrategy(IStrategy):
    # Define strategy parameters
    minimal_roi = {"0": 0.01}
    stoploss = -0.05
    timeframe = "5m"

    fastma = IntParameter(11, 15, default=10, space="buy")
    slowma = IntParameter(45, 55, default=50, space="buy")

    # # Buy hyperspace params:
    # buy_params = {
    #     "adx_long": 39,
    #     "adx_short": 20,
    #     "close_market_shift_long": 6,
    #     "close_market_shift_short": 9,
    #     "entryMA_tp": 8,
    #     "fastMA_tp": 16,
    #     "marketMA_tp": 97,
    #     "rsi_tp": 10,
    #     "slowMA_tp": 57,
    #     "leverage_num": 2,  # value loaded from strategy
    # }

    # # Sell hyperspace params:
    # sell_params = {
    #     "last_lowest_rolling_long": 9,
    #     "last_lowest_rolling_short": 9,
    # }

    protection_params = {
        "max_allowed_drawdown": 0.45,
        "max_drawdown_lookback": 102,
        "max_drawdown_stop_duration": 53,
        "max_drawdown_trade_limit": 14,
        "stoploss_guard_lookback": 157,
        "stoploss_guard_stop_duration": 191,
        "stoploss_guard_trade_limit": 18,
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ma_fast"] = dataframe["close"].rolling(window=self.fastma.value).mean()
        dataframe["ma_slow"] = dataframe["close"].rolling(window=self.slowma.value).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["ma_fast"] > dataframe["ma_slow"])
            & (dataframe["ma_fast"].shift(1) <= dataframe["ma_slow"].shift(1)),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["ma_fast"] < dataframe["ma_slow"])
            & (dataframe["ma_fast"].shift(1) >= dataframe["ma_slow"].shift(1)),
            "enter_short",
        ] = 1

        return dataframe
