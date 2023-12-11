from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

class TwoMovingAveragesStrategy(IStrategy):
    # Define strategy parameters
    minimal_roi = {"0": 0.01}
    stoploss = -0.05
    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate short-term (fast) moving average
        dataframe['ma_fast'] = dataframe['close'].rolling(window=10).mean()

        # Calculate long-term (slow) moving average
        dataframe['ma_slow'] = dataframe['close'].rolling(window=50).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Generate buy signal when ma_fast crosses above ma_slow
        dataframe.loc[
            (dataframe['ma_fast'] > dataframe['ma_slow']) &
            (dataframe['ma_fast'].shift(1) <= dataframe['ma_slow'].shift(1)),
            'enter_long'
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Generate sell signal when ma_fast crosses below ma_slow
        dataframe.loc[
            (dataframe['ma_fast'] < dataframe['ma_slow']) &
            (dataframe['ma_fast'].shift(1) >= dataframe['ma_slow'].shift(1)),
            'enter_short'
        ] = 1

        return dataframe
