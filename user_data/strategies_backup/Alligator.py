from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class Alligator(IStrategy):
    INTERFACE_VERSION: int = 3

    # Define strategy parameters
    minimal_roi = {"0": 0.01}
    stoploss = -0.10
    timeframe = '5m'
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate mas
        dataframe['ma_slow'] = dataframe['close'].rolling(window=self.slowma).mean()
        dataframe['ma_medium'] = dataframe['close'].rolling(window=self.mediumma).mean()
        dataframe['ma_fast'] = dataframe['close'].rolling(window=self.fastma).mean()
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Generate buy signal when ma_fast crosses above ma_slow
        dataframe.loc[
            (dataframe['close'] > dataframe['ma_fast']) &
            (dataframe['ma_fast'] > dataframe['ma_medium']) &
            (dataframe['ma_medium'] > dataframe['ma_slow']) &
            (dataframe['adx'] > 25),
            'enter_long'
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Generate sell signal when ma_fast crosses below ma_slow
        dataframe.loc[
            (dataframe['close'] < dataframe['ma_fast']) &
            (dataframe['ma_fast'] < dataframe['ma_medium']) &
            (dataframe['ma_medium'] < dataframe['ma_slow']) &
            (dataframe['adx'] > 25),
            'enter_short'
        ] = 1

        return dataframe
