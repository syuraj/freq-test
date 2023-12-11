# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
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

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


# custom indicators
# ##############################################################################################################################################################################################

def trade_signal(dataframe, rsi_tp = 14, bb_tp = 20):
    # Compute indicators
    dataframe['RSI'] = ta.RSI(dataframe['close'], timeperiod=rsi_tp)
    dataframe['upper_band'], dataframe['middle_band'], dataframe['lower_band'] = ta.BBANDS(dataframe['close'], timeperiod=bb_tp)
    dataframe['macd'], dataframe['signal'], _ = ta.MACD(dataframe['close'])

    # LONG Trade conditions
    conditions_long = ((dataframe['RSI'] > 50) & (dataframe['close'] > dataframe['middle_band']) & (dataframe['close'] < dataframe['upper_band']) & (dataframe['macd'] > dataframe['signal']) & ((dataframe['high'] - dataframe['close']) < (dataframe['close'] - dataframe['open'])) & (dataframe['close'] > dataframe['open']) )
    conditions_short = ((dataframe['RSI'] < 50) & (dataframe['close'] < dataframe['middle_band']) & (dataframe['close'] > dataframe['lower_band']) & (dataframe['macd'] < dataframe['signal']) & ((dataframe['close'] - dataframe['low']) < (dataframe['open'] - dataframe['close'])) & (dataframe['close'] < dataframe['open']) )

    # dataframe['signal'] = 0
    dataframe.loc[conditions_long, 'trend'] = 1
    dataframe.loc[conditions_short, 'trend'] = -1

    return dataframe

# ##############################################################################################################################################################################################

class RSI_BB_MACD_Nov_2023_1h_2_Dec(IStrategy):


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

    adx_long_max_1 = DecimalParameter(6.1, 10.0, default=6.5, decimals = 1, space="buy", optimize = parameters_yes)
    adx_long_max_2 = DecimalParameter(24.9, 60.0, default=50.7, decimals = 1, space="buy", optimize = parameters_yes)

    adx_long_min_1 = DecimalParameter(4.0, 6.0, default=5.7, decimals = 1, space="buy", optimize = parameters_yes)
    adx_long_min_2 = DecimalParameter(18.5, 21.0, default=20.9, decimals = 1, space="buy", optimize = parameters_yes)

    adx_short_max_1 = DecimalParameter(14.1, 21.9, default=21.4, decimals = 1, space="buy", optimize = parameters_yes)
    adx_short_max_2 = DecimalParameter(30.6, 55.0, default=50.8, decimals = 1, space="buy", optimize = parameters_yes)

    adx_short_min_1 = DecimalParameter(8.7, 14, default=9.9, decimals = 1, space="buy", optimize = parameters_yes)
    adx_short_min_2 = DecimalParameter(25.0, 30.5, default=30.3, decimals = 1, space="buy", optimize = parameters_yes)

    bb_tp_l = IntParameter(15, 35, default=16, space="buy", optimize= parameters_yes)
    bb_tp_s = IntParameter(15, 35, default=20, space="buy", optimize= parameters_yes)

    rsi_tp_l = IntParameter(10, 25, default=22, space="buy", optimize= parameters_yes)
    rsi_tp_s = IntParameter(10, 25, default=17, space="buy", optimize= parameters_yes)

    volume_check = IntParameter(10, 45, default=38, space="buy", optimize= parameters_yes)
    volume_check_s = IntParameter(15, 45, default=20, space="buy", optimize= parameters_yes)


    atr_long_mul = DecimalParameter(1.1, 6.0, default=3.8, decimals = 1, space="sell", optimize = parameters_yes)
    atr_short_mul = DecimalParameter(1.1, 6.0, default=5.0, decimals = 1, space="sell", optimize = parameters_yes)

    ema_period_l_exit = IntParameter(22, 200, default=91, space="sell", optimize= parameters_yes)
    ema_period_s_exit = IntParameter(22, 200, default=147, space="sell", optimize= parameters_yes)

    volume_check_exit = IntParameter(10, 45, default=19, space="sell", optimize= parameters_yes)
    volume_check_exit_s = IntParameter(15, 45, default=41, space="sell", optimize= parameters_yes)


    protect_optimize = True
    # cooldown_lookback = IntParameter(1, 40, default=4, space="protection", optimize=protect_optimize)
    max_drawdown_lookback = IntParameter(1, 50, default=2, space="protection", optimize=protect_optimize)
    max_drawdown_trade_limit = IntParameter(1, 3, default=1, space="protection", optimize=protect_optimize)
    max_drawdown_stop_duration = IntParameter(1, 50, default=4, space="protection", optimize=protect_optimize)
    max_allowed_drawdown = DecimalParameter(0.05, 0.30, default=0.10, decimals=2, space="protection",
                                            optimize=protect_optimize)
    stoploss_guard_lookback = IntParameter(1, 50, default=8, space="protection", optimize=protect_optimize)
    stoploss_guard_trade_limit = IntParameter(1, 3, default=1, space="protection", optimize=protect_optimize)
    stoploss_guard_stop_duration = IntParameter(1, 50, default=4, space="protection", optimize=protect_optimize)

    @property
    def protections(self):
        return [
            # {
            #     "method": "CooldownPeriod",
            #     "stop_duration_candles": self.cooldown_lookback.value
            # },
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": self.max_drawdown_lookback.value,
                "trade_limit": self.max_drawdown_trade_limit.value,
                "stop_duration_candles": self.max_drawdown_stop_duration.value,
                "max_allowed_drawdown": self.max_allowed_drawdown.value
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": self.stoploss_guard_lookback.value,
                "trade_limit": self.stoploss_guard_trade_limit.value,
                "stop_duration_candles": self.stoploss_guard_stop_duration.value,
                "only_per_pair": False
            }
        ]




    # ema_long = IntParameter(50, 250, default=100, space="buy")
    # ema_short = IntParameter(50, 250, default=100, space="buy")

    # sell_rsi = IntParameter(60, 90, default=70, space="sell")

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }

    @property
    def plot_config(self):
        return {
            # Main plot indicators (Moving averages, ...)
            'main_plot': {
                'tema': {},
                'sar': {'color': 'white'},
            },
            'subplots': {
                # Subplots - each dict defines one additional plot
                "MACD": {
                    'macd': {'color': 'blue'},
                    'macdsignal': {'color': 'orange'},
                },
                "RSI": {
                    'rsi': {'color': 'red'},
                }
            }
        }



    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        if not self.dp:
            # Don't do anything if DataProvider is not available.
            return dataframe

        L_optimize_trend_alert  = trade_signal(dataframe=dataframe, rsi_tp= self.rsi_tp_l.value, bb_tp = self.bb_tp_l.value )
        dataframe['trend_l'] = L_optimize_trend_alert['trend']

        S_optimize_trend_alert  = trade_signal(dataframe=dataframe, rsi_tp= self.rsi_tp_s.value, bb_tp = self.bb_tp_s.value )
        dataframe['trend_s'] = S_optimize_trend_alert['trend']

        # ADX
        dataframe['adx'] = ta.ADX(dataframe)

        # ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=20)

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
                        (
                            (dataframe['adx'] > self.adx_long_min_1.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_long_max_1.value)
                        ) |
                        (
                            (dataframe['adx'] > self.adx_long_min_2.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_long_max_2.value)
                        ) & # trend strength confirmation
                        (dataframe['trend_l'] == 1) &
                        (dataframe['volume'] > dataframe['volume_mean'])
                        # (dataframe['volume'] > 0)

            ),
            'enter_long'] = 1

        dataframe.loc[
            (
                        (
                            (dataframe['adx'] > self.adx_short_min_1.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_short_max_1.value)
                        ) |
                        (
                            (dataframe['adx'] > self.adx_short_min_2.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_short_max_2.value)
                        ) & # trend strength confirmation
                        (dataframe['trend_s'] == -1) &
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
                (dataframe['close'] < (dataframe['ema_l'] - (self.atr_long_mul.value * dataframe['atr']))) &
                (dataframe['volume'] > dataframe['volume_mean_exit'])
        )

        exit_short = (
                # (dataframe['close'] > dataframe['high'].shift(self.sell_shift_short.value)) &
                (dataframe['close'] > (dataframe['ema_s'] + (self.atr_short_mul.value * dataframe['atr']))) &
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

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, side: str,
                 **kwargs) -> float:

        return self.leverage_num.value
