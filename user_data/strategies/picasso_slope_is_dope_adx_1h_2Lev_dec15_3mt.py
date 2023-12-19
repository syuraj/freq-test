# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class picasso_slope_is_dope_adx_1h_2Lev_dec15_3mt(IStrategy):

    '''
    max-trades : 3

            freqtrade backtesting --strategy picasso_slope_is_dope_adx_1h_2Lev_dec15_3mt -i 1h --export trades --breakdown month --timerange 20211101-20221208
            freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy picasso_slope_is_dope_adx_1h_2Lev_dec15_3mt -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102

                =========================================================== ENTER TAG STATS ===========================================================
                |   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
                |-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
                | TOTAL |      3814 |           0.85 |        3238.63 |          4845.917 |         484.59 |        2:35:00 |  2752     0  1062  72.2 |
                ======================================================= EXIT REASON STATS ========================================================
                |        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
                |--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
                | trailing_stop_loss |    2828 |   2686     0   142  95.0 |           2.75 |        7785.19 |         11631.5   |        2595.06 |
                |        exit_signal |     904 |     10     0   894   1.1 |          -6.05 |       -5472.23 |         -8174.27  |       -1824.08 |
                |                roi |      69 |     55     0    14  79.7 |          17.63 |        1216.64 |          1821.33  |         405.55 |
                |          stop_loss |      10 |      0     0    10     0 |         -28.95 |        -289.5  |          -430.463 |         -96.5  |
                |         force_exit |       3 |      1     0     2  33.3 |          -0.49 |          -1.48 |            -2.212 |          -0.49 |
                ======================================================== LEFT OPEN TRADES REPORT =========================================================
                |     Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
                |----------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
                | ZEN/USDT |         1 |           0.42 |           0.42 |             0.628 |           0.06 |        7:00:00 |     1     0     0   100 |
                | ZEC/USDT |         1 |          -0.22 |          -0.22 |            -0.326 |          -0.03 |        6:00:00 |     0     0     1     0 |
                |  AR/USDT |         1 |          -1.68 |          -1.68 |            -2.513 |          -0.25 |        1:00:00 |     0     0     1     0 |
                |    TOTAL |         3 |          -0.49 |          -1.48 |            -2.212 |          -0.22 |        4:40:00 |     1     0     2  33.3 |
                ======================= MONTH BREAKDOWN ========================
                |      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
                |------------+-------------------+--------+---------+----------|
                | 31/01/2022 |           518.64  |    280 |       0 |       87 |
                | 28/02/2022 |           253.151 |    216 |       0 |       90 |
                | 31/03/2022 |           781.56  |    352 |       0 |      107 |
                | 30/04/2022 |           354.388 |    238 |       0 |       77 |
                | 31/05/2022 |          1166.55  |    292 |       0 |       67 |
                | 30/06/2022 |           209.446 |    189 |       0 |       58 |
                | 31/07/2022 |           417.505 |    325 |       0 |      119 |
                | 31/08/2022 |           321.697 |    220 |       0 |      101 |
                | 30/09/2022 |           -30.796 |    157 |       0 |       89 |
                | 31/10/2022 |           163.703 |    214 |       0 |      132 |
                | 30/11/2022 |           567.286 |    212 |       0 |       84 |
                | 31/12/2022 |           122.791 |     57 |       0 |       51 |
                ================== SUMMARY METRICS ==================
                | Metric                      | Value               |
                |-----------------------------+---------------------|
                | Backtesting from            | 2022-01-01 00:00:00 |
                | Backtesting to              | 2022-12-08 00:00:00 |
                | Max open trades             | 3                   |
                |                             |                     |
                | Total/Daily Avg Trades      | 3814 / 11.18        |
                | Starting balance            | 1000 USDT           |
                | Final balance               | 5845.917 USDT       |
                | Absolute profit             | 4845.917 USDT       |
                | Total profit %              | 484.59%             |
                | CAGR %                      | 561.95%             |
                | Profit factor               | 1.53                |
                | Trades per day              | 11.18               |
                | Avg. daily profit %         | 1.42%               |
                | Avg. stake amount           | 149.366 USDT        |
                | Total trade volume          | 569682.426 USDT     |
                |                             |                     |
                | Long / Short                | 2397 / 1417         |
                | Total profit Long %         | 348.13%             |
                | Total profit Short %        | 136.47%             |
                | Absolute profit Long        | 3481.267 USDT       |
                | Absolute profit Short       | 1364.65 USDT        |
                |                             |                     |
                | Best Pair                   | GMT/USDT 226.73%    |
                | Worst Pair                  | BAL/USDT -45.58%    |
                | Best trade                  | CELO/USDT 29.82%    |
                | Worst trade                 | AAVE/USDT -29.03%   |
                | Best day                    | 231.141 USDT        |
                | Worst day                   | -71.979 USDT        |
                | Days win/draw/lose          | 187 / 54 / 95       |
                | Avg. Duration Winners       | 1:31:00             |
                | Avg. Duration Loser         | 5:21:00             |
                | Rejected Entry signals      | 361560              |
                | Entry/Exit Timeouts         | 0 / 508             |
                |                             |                     |
                | Min balance                 | 953.364 USDT        |
                | Max balance                 | 5862.83 USDT        |
                | Max % of account underwater | 6.01%               |
                | Absolute Drawdown (Account) | 3.51%               |
                | Absolute Drawdown           | 180.58 USDT         |
                | Drawdown high               | 4143.184 USDT       |
                | Drawdown low                | 3962.604 USDT       |
                | Drawdown Start              | 2022-09-10 08:00:00 |
                | Drawdown End                | 2022-10-02 00:00:00 |
                | Market change               | -76.77%             |
                =====================================================

                2022-12-14 06:18:09,580 - NostalgiaForInfinityX_dec13_15m - INFO - pandas_ta successfully imported
                2022-12-14 06:18:09,686 - freqtrade.optimize.hyperopt_tools - INFO - Dumping parameters to /freqtrade/user_data/strategies/slope_is_dope_adx_1h_2Lev_dec14.json

                Epoch details:

                139/155:   3814 trades. 2752/0/1062 Wins/Draws/Losses. Avg profit   0.85%. Median profit   2.26%. Total profit 4845.91739859 USDT ( 484.59%). Avg duration 2:35:00 min. Objective: -30.40069


                    # Buy hyperspace params:
                    buy_params = {
                        "adx_long": 39,
                        "adx_short": 20,
                        "close_market_shift_long": 6,
                        "close_market_shift_short": 9,
                        "entryMA_tp": 8,
                        "fastMA_tp": 16,
                        "marketMA_tp": 97,
                        "rsi_tp": 10,
                        "slowMA_tp": 57,
                        "leverage_num": 2,  # value loaded from strategy
                    }

                    # Sell hyperspace params:
                    sell_params = {
                        "last_lowest_rolling_long": 9,
                        "last_lowest_rolling_short": 9,
                    }

                    # Protection hyperspace params:
                    protection_params = {
                        "max_allowed_drawdown": 0.45,
                        "max_drawdown_lookback": 102,
                        "max_drawdown_stop_duration": 53,
                        "max_drawdown_trade_limit": 14,
                        "stoploss_guard_lookback": 157,
                        "stoploss_guard_stop_duration": 191,
                        "stoploss_guard_trade_limit": 18,
                    }

                    # ROI table:
                    minimal_roi = {
                        "0": 0.283,
                        "132": 0.16,
                        "548": 0.071,
                        "961": 0
                    }

                    # Stoploss:
                    stoploss = -0.289

                    # Trailing stop:
                    trailing_stop = True
                    trailing_stop_positive = 0.01
                    trailing_stop_positive_offset = 0.021
                    trailing_only_offset_is_reached = True



    '''

    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '1h'

    # Can this strategy go short?
    can_short: bool = True


    minimal_roi = {
        "0": 0.283,
        "132": 0.16,
        "548": 0.071,
        "961": 0
    }


    stoploss = -0.289

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.021
    trailing_only_offset_is_reached = True

    '''

    '''

    #leverage here
    leverage_optimize = False
    leverage_num = IntParameter(low=1, high=5, default=2, space='buy', optimize=leverage_optimize)

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Strategy parameters
    # buy_rsi = IntParameter(10, 40, default=30, space="buy")
    # sell_rsi = IntParameter(60, 90, default=70, space="sell")
    close_market_shift_long = IntParameter(5,15,default=6,space="buy")
    close_market_shift_short = IntParameter(5,15,default=9,space="buy")

    entryMA_tp = IntParameter(1,10, default=8, space="buy")
    fastMA_tp = IntParameter(10,30, default=16, space="buy")
    marketMA_tp = IntParameter(95,220, default=97, space="buy")
    rsi_tp = IntParameter(5,20, default=10, space="buy")
    slowMA_tp = IntParameter(30,60, default=57, space="buy")
    adx_long = IntParameter(15,50, default=39, space="buy")
    adx_short = IntParameter(15,50, default=20, space="buy")

    # rsi_value_long = IntParameter(30,80, default=55, space="buy")
    # rsi_value_short = IntParameter(30,80, default=55, space="buy")

    last_lowest_rolling_long = IntParameter(5,20,default=9, space="sell")
    last_lowest_rolling_short = IntParameter(5,20,default=9, space="sell")


    # protection
    protect_optimize = True
    # cooldown_lookback = IntParameter(1, 240, default=6, space="protection", optimize=protect_optimize)
    max_drawdown_lookback = IntParameter(1, 288, default=8, space="protection", optimize=protect_optimize)
    max_drawdown_trade_limit = IntParameter(1, 20, default=1, space="protection", optimize=protect_optimize)
    max_drawdown_stop_duration = IntParameter(1, 288, default=8, space="protection", optimize=protect_optimize)
    max_allowed_drawdown = DecimalParameter(0.10, 0.50, default=0.12, decimals=2, space="protection",
                                            optimize=protect_optimize)
    stoploss_guard_lookback = IntParameter(1, 288, default=10, space="protection", optimize=protect_optimize)
    stoploss_guard_trade_limit = IntParameter(1, 20, default=1, space="protection", optimize=protect_optimize)
    stoploss_guard_stop_duration = IntParameter(1, 288, default=8, space="protection", optimize=protect_optimize)

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
            "main_plot": {
            # Configuration for main plot indicators.
            "fastMA": {"color": "red"},
            "slowMA": {"color": "blue"},
            },
            "subplots": {
            # Additional subplots
            "rsi": {"rsi": {"color": "blue"}},
            "fast_slope": {"fast_slope": {"color": "red"}, "slow_slope": {"color": "blue"}},
            },
        }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.rsi_tp.value)
        dataframe['marketMA'] = ta.SMA(dataframe, timeperiod=self.marketMA_tp.value)
        dataframe['fastMA'] = ta.SMA(dataframe, timeperiod=self.fastMA_tp.value)
        dataframe['slowMA'] = ta.SMA(dataframe, timeperiod=self.slowMA_tp.value)
        dataframe['entryMA'] = ta.SMA(dataframe, timeperiod=self.slowMA_tp.value)
        dataframe['adx'] = ta.ADX(dataframe)

        # Calculate slope of slowMA
        # See: https://www.wikihow.com/Find-the-Slope-of-a-Line
        dataframe['sy1'] = dataframe['slowMA'].shift(+11)
        dataframe['sy2'] = dataframe['slowMA'].shift(+1)
        sx1 = 1
        sx2 = 11
        dataframe['sy'] = dataframe['sy2'] - dataframe['sy1']
        dataframe['sx'] = sx2 - sx1
        dataframe['slow_slope'] = dataframe['sy']/dataframe['sx']
        dataframe['fy1'] = dataframe['fastMA'].shift(+11)
        dataframe['fy2'] = dataframe['fastMA'].shift(+1)
        fx1 = 1
        fx2 = 11
        dataframe['fy'] = dataframe['fy2'] - dataframe['fy1']
        dataframe['fx'] = fx2 - fx1
        dataframe['fast_slope'] = dataframe['fy']/dataframe['fx']
        # print(dataframe[['date','close', 'slow_slope','fast_slope']].tail(50))

        # ==== Trailing custom stoploss indicator ====
        dataframe['last_lowest_long'] = dataframe['low'].rolling(self.last_lowest_rolling_long.value).min().shift(1)
        dataframe['last_lowest_short'] = dataframe['low'].rolling(self.last_lowest_rolling_short.value).min().shift(1)



        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        dataframe.loc[
            (
                (
                (dataframe['adx'] > self.adx_long.value) &
                (dataframe['close'] > dataframe['marketMA']) &
                # Only trade when the fast slope is above 0
                (dataframe['fast_slope'] > 0) &
                # Only trade when the slow slope is above 0
                (dataframe['slow_slope'] > 0) &
                # Only buy when the close price is higher than the 3day average of ten periods ago
                # (dataframe['close'] > dataframe['entryMA'].shift(+11)) &
                # Or only buy when the close price is higher than the close price of 3 days ago (this is a choice)
                (dataframe['close'] > dataframe['close'].shift(self.close_market_shift_long.value)) &
                # Only enter trades when the RSI is higher than 55
                (dataframe['rsi'] > 55) &
                # Only trade when the fast MA is above the slow MA
                (dataframe['fastMA'] > dataframe['slowMA'])
                # Or trade when the fase MA crosses above the slow MA (This is a choice...)
                # (qtpylib.crossed_above(dataframe['fastMA'], dataframe['slowMA']))
                )
            ),
            'enter_long'] = 1
        # Uncomment to use shorts (Only used in futures/margin mode. Check the documentation for more info)

        dataframe.loc[
            (
                (
                (dataframe['adx'] > self.adx_short.value) &
                (dataframe['close'] < dataframe['marketMA']) &
                # Only trade when the fast slope is above 0
                (dataframe['fast_slope'] < 0) &
                # Only trade when the slow slope is above 0
                (dataframe['slow_slope'] < 0) &
                # Only buy when the close price is higher than the 3day average of ten periods ago
                # (dataframe['close'] > dataframe['entryMA'].shift(+11)) &
                # Or only buy when the close price is higher than the close price of 3 days ago (this is a choice)
                (dataframe['close'] < dataframe['close'].shift(self.close_market_shift_short.value)) &
                # Only enter trades when the RSI is higher than 55
                (dataframe['rsi'] < 55) &
                # Only trade when the fast MA is above the slow MA
                (dataframe['fastMA'] < dataframe['slowMA'])
                # Or trade when the fase MA crosses above the slow MA (This is a choice...)
                # (qtpylib.crossed_above(dataframe['fastMA'], dataframe['slowMA']))
                )
            ),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        dataframe.loc[
            (
                # Close or do not trade when fastMA is below slowMA
                (dataframe['fastMA'] < dataframe['slowMA'])
                # Or close position when the close price gets below the last lowest candle price configured
                # (AKA candle based (Trailing) stoploss)
                | (dataframe['close'] < dataframe['last_lowest_long'])
                # | (dataframe['close'] < dataframe['fastMA'])
            ),
            'exit_long'] = 1
        # Uncomment to use shorts (Only used in futures/margin mode. Check the documentation for more info)

        dataframe.loc[
            (
                # Close or do not trade when fastMA is below slowMA
                (dataframe['fastMA'] > dataframe['slowMA'])
                # Or close position when the close price gets below the last lowest candle price configured
                # (AKA candle based (Trailing) stoploss)
                | (dataframe['close'] > dataframe['last_lowest_short'])
                # | (dataframe['close'] < dataframe['fastMA'])
            ),
            'exit_short'] = 1

        return dataframe


    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, side: str,
                 **kwargs) -> float:

        return self.leverage_num.value
