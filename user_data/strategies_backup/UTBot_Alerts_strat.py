# %%
# Import libraries

from cmath import nan
from functools import reduce
from math import sqrt
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.persistence import Trade

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, stoploss_from_open, DecimalParameter,
                                IntParameter, IStrategy, informative, merge_informative_pair)


import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


# %%
# custom indicators
def UTBot_Alerts(dataframe, key_value=1, atr_period=3, ema_period=200):
    # Calculate ATR and xATRTrailingStop
    xATR = np.array(ta.ATR(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=atr_period))
    nLoss = key_value * xATR
    src = dataframe['close']

    # Initialize arrays
    xATRTrailingStop = np.zeros(len(dataframe))
    xATRTrailingStop[0] = src[0] - nLoss[0]

    # Calculate xATRTrailingStop using vectorized operations
    mask_1 = (src > np.roll(xATRTrailingStop, 1)) & (np.roll(src, 1) > np.roll(xATRTrailingStop, 1))
    mask_2 = (src < np.roll(xATRTrailingStop, 1)) & (np.roll(src, 1) < np.roll(xATRTrailingStop, 1))
    mask_3 = src > np.roll(xATRTrailingStop, 1)

    xATRTrailingStop = np.where(mask_1, np.maximum(np.roll(xATRTrailingStop, 1), src - nLoss), xATRTrailingStop)
    xATRTrailingStop = np.where(mask_2, np.minimum(np.roll(xATRTrailingStop, 1), src + nLoss), xATRTrailingStop)
    xATRTrailingStop = np.where(mask_3, src - nLoss, xATRTrailingStop)

    mask_buy = (np.roll(src, 1) < xATRTrailingStop) & (src > np.roll(xATRTrailingStop, 1))
    mask_sell = (np.roll(src, 1) > xATRTrailingStop) & (src < np.roll(xATRTrailingStop, 1))

    pos = np.zeros(len(dataframe))
    pos = np.where(mask_buy, 1, pos)
    pos = np.where(mask_sell, -1, pos)
    pos[~((pos == 1) | (pos == -1))] = 0

    ema = np.array(ta.EMA(dataframe['close'], timeperiod=ema_period))

    buy_condition_utbot = (xATRTrailingStop > ema) & (pos > 0) & (src > ema)
    sell_condition_utbot = (xATRTrailingStop < ema) & (pos < 0) & (src < ema)

    trend = np.where(buy_condition_utbot, 1, np.where(sell_condition_utbot, -1, 0))

    trend = np.array(trend)

    dataframe['trend'] = trend
    return dataframe

def optimize_trend_alert(dataframe, key_value=1, atr_period=3, ema_period=200):
    # Calculate ATR and xATRTrailingStop
    xATR = np.array(ta.ATR(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=atr_period))
    nLoss = key_value * xATR
    src = dataframe['close']

    # Initialize arrays
    xATRTrailingStop = np.zeros(len(dataframe))
    xATRTrailingStop[0] = src[0] - nLoss[0]

    # Calculate xATRTrailingStop using vectorized operations
    mask_1 = (src > np.roll(xATRTrailingStop, 1)) & (np.roll(src, 1) > np.roll(xATRTrailingStop, 1))
    mask_2 = (src < np.roll(xATRTrailingStop, 1)) & (np.roll(src, 1) < np.roll(xATRTrailingStop, 1))
    mask_3 = src > np.roll(xATRTrailingStop, 1)

    xATRTrailingStop = np.where(mask_1, np.maximum(np.roll(xATRTrailingStop, 1), src - nLoss), xATRTrailingStop)
    xATRTrailingStop = np.where(mask_2, np.minimum(np.roll(xATRTrailingStop, 1), src + nLoss), xATRTrailingStop)
    xATRTrailingStop = np.where(mask_3, src - nLoss, xATRTrailingStop)

    # Calculate pos using vectorized operations
    mask_buy = (np.roll(src, 1) < xATRTrailingStop) & (src > np.roll(xATRTrailingStop, 1))
    mask_sell = (np.roll(src, 1) > xATRTrailingStop)  & (src < np.roll(xATRTrailingStop, 1))

    pos = np.zeros(len(dataframe))
    pos = np.where(mask_buy, 1, pos)
    pos = np.where(mask_sell, -1, pos)
    pos[~((pos == 1) | (pos == -1))] = 0

    ema = np.array(ta.EMA(dataframe['close'], timeperiod=ema_period))

    buy_condition_utbot = (xATRTrailingStop > ema) & (pos > 0) & (src > ema)
    sell_condition_utbot = (xATRTrailingStop < ema) & (pos < 0) & (src < ema)

    trend = np.where(buy_condition_utbot, 1, np.where(sell_condition_utbot, -1, 0))

    trend = np.array(trend)

    dataframe['trend'] = trend
    return dataframe

class UTBot_Alerts_strat(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '1h'

    # Can this strategy go short?
    can_short = True

    # risk_c = DecimalParameter(0.025, 0.01, 0.1, decimals=2, space='buy')

    # Minimal ROI designed for the strategy.
    minimal_roi = {
    #   "0": 0.282,
    #   "138": 0.179,
    #   "310": 0.089,
    #   "877": 0
    # '0': 0.344, '260': 0.225, '486': 0.09, '796': 0
    "0": 0.184,
    "416": 0.14,
    "933": 0.073,
    "1982": 0

    #   '0': 0.279, '154': 0.122, '376': 0.085, '456': 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.317

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.022
    trailing_only_offset_is_reached = True

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    #leverage here
    leverage_optimize = True
    leverage_num = IntParameter(low=1, high=5, default=5, space='buy', optimize=leverage_optimize)

    # Strategy parameters
    parameters_yes = True
    parameters_no = False

    key_value_l = IntParameter(1, 50, default=2, space="protection", optimize=True)
    key_value_s = IntParameter(1, 50, default=4, space="protection", optimize=True)

    atr_period_l = IntParameter(10, 200, default=7, space="signal", optimize=True)
    atr_period_s = IntParameter(10, 200, default=10, space="signal", optimize=True)

    ema_period_l = IntParameter(10, 200, default=10, space="signal", optimize=True)
    ema_period_s = IntParameter(10, 200, default=50, space="signal", optimize=True)

    ema_period_l_exit = IntParameter(10, 200, default=10, space="signal", optimize=True)
    ema_period_s_exit = IntParameter(10, 200, default=50, space="signal", optimize=True)

    volume_check = IntParameter(10, 200, default=10, space="signal", optimize=True)
    volume_check_s = IntParameter(10, 200, default=50, space="signal", optimize=True)
    volume_check_exit = IntParameter(10, 200, default=50, space="signal", optimize=True)
    volume_check_exit_s = IntParameter(10, 200, default=50, space="signal", optimize=True)

    def custom_strategy(dataframe):
        dataframe = UTBot_Alerts(dataframe, key_value=2, atr_period=7, ema_period=100)

        # Calculate RSI and ADX
        rsi = ta.RSI(dataframe['close'])
        adx = ta.ADX(dataframe['high'], dataframe['low'], dataframe['close'])

        # Define conditions based on UTBot Alerts and additional indicators
        # ... (your custom conditions here)

        return dataframe



    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        if not self.dp:
            # Don't do anything if DataProvider is not available.
            return dataframe

        L_optimize_trend_alert  = optimize_trend_alert(dataframe=dataframe, key_value= self.key_value_l.value, atr_period= self.atr_period_l.value, ema_period=self.ema_period_l.value)
        dataframe['trend_l'] = L_optimize_trend_alert['trend']

        S_optimize_trend_alert  = optimize_trend_alert(dataframe=dataframe, key_value= self.key_value_s.value, atr_period= self.atr_period_s.value, ema_period=self.ema_period_s.value)
        dataframe['trend_s'] = S_optimize_trend_alert['trend']

        # ADX
        dataframe['adx'] = ta.ADX(dataframe)

        # RSI
        # dataframe['rsi'] = ta.RSI(dataframe)

        # EMA
        dataframe['ema_l'] = ta.EMA(dataframe['close'], timeperiod=self.ema_period_l_exit.value)
        dataframe['ema_s'] = ta.EMA(dataframe['close'], timeperiod=self.ema_period_s_exit.value)

        # Volume Weighted
        dataframe['volume_mean'] = dataframe['volume'].rolling(self.volume_check.value).mean().shift(1)
        dataframe['volume_mean_exit'] = dataframe['volume'].rolling(self.volume_check_exit.value).mean().shift(1)

        dataframe['volume_mean_s'] = dataframe['volume'].rolling(self.volume_check_s.value).mean().shift(1)
        dataframe['volume_mean_exit_s'] = dataframe['volume'].rolling(self.volume_check_exit_s.value).mean().shift(1)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                        (dataframe['adx'] > self.adx_long_min.value) & # trend strength confirmation
                        (dataframe['adx'] < self.adx_long_max.value) & # trend strength confirmation
                        (dataframe['trend_l'] > 0) &
                        (dataframe['volume'] > dataframe['volume_mean']) &
                        (dataframe['volume'] > 0)

            ),
            'enter_long'] = 1

        dataframe.loc[
            (
                        (dataframe['adx'] > self.adx_short_min.value) & # trend strength confirmation
                        (dataframe['adx'] < self.adx_short_max.value) & # trend strength confirmation
                        (dataframe['trend_s'] < 0) &
                        (dataframe['volume'] > dataframe['volume_mean_s']) # volume weighted indicator
            ),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []
        conditions_short = []
        dataframe.loc[:, 'exit_tag'] = ''

        exit_long = (
                # (dataframe['close'] < dataframe['low'].shift(self.sell_shift.value)) &
                (dataframe['close'] < dataframe['ema_l']) &
                (dataframe['volume'] > dataframe['volume_mean_exit'])
        )

        exit_short = (
                # (dataframe['close'] > dataframe['high'].shift(self.sell_shift_short.value)) &
                (dataframe['close'] > dataframe['ema_s']) &
                (dataframe['volume'] > dataframe['volume_mean_exit_s'])
        )

        conditions_short.append(exit_short)
        dataframe.loc[exit_short, 'exit_tag'] += 'exit_short'

        conditions_long.append(exit_long)
        dataframe.loc[exit_long, 'exit_tag'] += 'exit_long'

        if conditions_long:
            dataframe.loc[
                reduce(lambda x, y: x | y, conditions_long),
                'exit_long'] = 1

        if conditions_short:
            dataframe.loc[
                reduce(lambda x, y: x | y, conditions_short),
                'exit_short'] = 1

        return dataframe
