from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
from freqtrade.persistence import Trade
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, stoploss_from_open, DecimalParameter,
                                IntParameter, IStrategy, informative, merge_informative_pair)

class Alligator(IStrategy):
    INTERFACE_VERSION: int = 3

    # Define strategy parameters
    minimal_roi = {"0": 0.01}
    stoploss = -0.10
    timeframe = '5m'
    startup_candle_count: int = 30

    can_short = True
    use_entry_signal = True
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    protect_optimize = True

    slowma = IntParameter(11, 15, default=13, space="buy")
    mediumma = IntParameter(6, 10, default=8, space="buy")
    fastma = IntParameter(3, 7, default=5, space="buy")
    adxPeriod = IntParameter(12, 16, default=14, space="buy")
    adxfilter = IntParameter(15, 30, default=20, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        print("printing self.slowma")
        print(self.slowma)
        dataframe['ma_slow'] = dataframe['close'].rolling(window=self.slowma.value).mean()
        dataframe['ma_medium'] = dataframe['close'].rolling(window=self.mediumma.value).mean()
        dataframe['ma_fast'] = dataframe['close'].rolling(window=self.fastma.value).mean()
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=self.adxPeriod.value)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Generate buy signal when ma_fast crosses above ma_slow
        dataframe.loc[
            (dataframe['close'] > dataframe['ma_fast']) &
            (dataframe['ma_fast'] > dataframe['ma_medium']) &
            (dataframe['ma_medium'] > dataframe['ma_slow']) &
            (dataframe['adx'] > self.adxfilter.value),
            'enter_long'
        ] = 1

        # Generate sell signal when ma_fast crosses below ma_slow
        dataframe.loc[
            (dataframe['close'] < dataframe['ma_fast']) &
            (dataframe['ma_fast'] < dataframe['ma_medium']) &
            (dataframe['ma_medium'] < dataframe['ma_slow']) &
            (dataframe['adx'] > self.adxfilter.value),
            'enter_short'
        ] = 1
        print(dataframe)

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Generate exit long when price closes below ma_medium
        dataframe.loc[
            (dataframe['close'] < dataframe['ma_medium']),
            'exit_long'
        ] = 1

        # Generate exit short when price above ma_medium
        dataframe.loc[
            (dataframe['close'] > dataframe['ma_medium']),
            'exit_short'
        ] = 1

        return dataframe
