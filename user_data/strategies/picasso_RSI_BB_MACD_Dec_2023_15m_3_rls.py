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

class picasso_RSI_BB_MACD_Dec_2023_15m_3_rls(IStrategy):


    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '15m'

    # Can this strategy go short?
    can_short = True


    '''





sudo docker compose run freqtrade backtesting --strategy RSI_BB_MACD_Dec_2023_15m_3_rls -i 5m --export trades --breakdown month --timerange 20230101-20231212

2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 5m.
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 20.
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'entry': 10, 'exit': 10, 'exit_timeout_count': 0, 'unit': 'minutes'}.
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'max_open_trades' with value in config file: 4.
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.184, '416': 0.14, '933': 0.073, '1982': 0}
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 5m
2023-12-18 06:05:24,661 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.317
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: True
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive: 0.012
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.03
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: True
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: False
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: True
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'entry': 'GTC', 'exit': 'GTC'}
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2023-12-18 06:05:24,662 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 20



2023-12-18 06:06:43,786 - freqtrade.optimize.backtesting - INFO - Loading data from 2022-12-31 21:30:00 up to 2023-12-12 00:00:00 (345 days).
2023-12-18 06:06:44,905 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2023-12-18 06:06:44,955 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy RSI_BB_MACD_Dec_2023_15m_3_rls
2023-12-18 06:06:44,955 - freqtrade.strategy.hyper - INFO - No params for buy found, using default values.
2023-12-18 06:06:44,955 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_max_1 = 6.5
2023-12-18 06:06:44,955 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_max_2 = 50.7
2023-12-18 06:06:44,955 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_min_1 = 5.7
2023-12-18 06:06:44,955 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_min_2 = 20.9
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_max_1 = 21.4
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_max_2 = 50.8
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_min_1 = 9.9
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_min_2 = 30.3
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): bb_tp_l = 16
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): bb_tp_s = 20
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): leverage_num = 5
2023-12-18 06:06:44,956 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): rsi_tp_l = 22
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): rsi_tp_s = 17
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check = 38
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_s = 20
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - No params for sell found, using default values.
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): atr_long_mul = 3.8
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): atr_short_mul = 5.0
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): ema_period_l_exit = 91
2023-12-18 06:06:44,957 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): ema_period_s_exit = 147
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_exit = 19
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_exit_s = 41
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - No params for protection found, using default values.
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_allowed_drawdown = 0.1
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_lookback = 2
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_stop_duration = 4
2023-12-18 06:06:44,958 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_trade_limit = 1
2023-12-18 06:06:44,959 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_lookback = 8
2023-12-18 06:06:44,959 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_stop_duration = 4
2023-12-18 06:06:44,959 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_trade_limit = 1
2023-12-18 06:06:48,459 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2023-01-01 00:00:00 up to 2023-12-12 00:00:00 (345 days).
2023-12-18 06:20:38,319 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-12-18_06-20-38.meta.json"
2023-12-18 06:20:38,324 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-12-18_06-20-38.json"
2023-12-18 06:20:38,856 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy RSI_BB_MACD_Dec_2023_15m_3_rls
================================================================ BACKTESTING REPORT ================================================================
|               Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|--------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|      OGN/USDT:USDT |       894 |           0.69 |         618.56 |           123.647 |          12.36 |        2:46:00 |   729     0   165  81.5 |
|      C98/USDT:USDT |       746 |           0.41 |         306.41 |            61.217 |           6.12 |        2:35:00 |   602     0   144  80.7 |
|     CELR/USDT:USDT |       440 |           0.60 |         262.26 |            52.444 |           5.24 |        2:06:00 |   346     0    94  78.6 |
|     UNFI/USDT:USDT |       317 |           0.79 |         248.88 |            49.656 |           4.97 |        2:33:00 |   259     0    58  81.7 |
|     CELO/USDT:USDT |      1109 |           0.19 |         206.22 |            41.211 |           4.12 |        4:04:00 |   920     0   189  83.0 |
|      SNX/USDT:USDT |       725 |           0.26 |         186.69 |            37.221 |           3.72 |        2:32:00 |   578     0   147  79.7 |
|      LPT/USDT:USDT |      1369 |           0.10 |         136.35 |            27.220 |           2.72 |        2:53:00 |  1084     0   285  79.2 |
|      FIL/USDT:USDT |        84 |           1.43 |         120.22 |            23.987 |           2.40 |        2:36:00 |    70     0    14  83.3 |
|      ATA/USDT:USDT |       148 |           0.51 |          75.07 |            14.989 |           1.50 |        2:57:00 |   121     0    27  81.8 |
|    STORJ/USDT:USDT |       171 |           0.44 |          75.09 |            14.973 |           1.50 |        2:14:00 |   133     0    38  77.8 |
|     ATOM/USDT:USDT |       352 |           0.20 |          69.87 |            13.952 |           1.40 |        3:44:00 |   264     0    88  75.0 |
|      KSM/USDT:USDT |       885 |           0.08 |          72.37 |            13.550 |           1.35 |        3:18:00 |   664     0   221  75.0 |
| 1000SHIB/USDT:USDT |       153 |           0.28 |          43.49 |             8.697 |           0.87 |        3:22:00 |   117     0    36  76.5 |
|      FTM/USDT:USDT |       109 |           0.18 |          19.15 |             3.822 |           0.38 |        2:37:00 |    84     0    25  77.1 |
|    ALPHA/USDT:USDT |       201 |           0.09 |          18.21 |             3.659 |           0.37 |        2:13:00 |   150     0    51  74.6 |
|     DENT/USDT:USDT |       118 |           0.10 |          11.23 |             2.242 |           0.22 |        2:48:00 |    94     0    24  79.7 |
|   PEOPLE/USDT:USDT |      1078 |          -0.02 |         -20.35 |            -4.074 |          -0.41 |        3:14:00 |   839     0   239  77.8 |
|     BAKE/USDT:USDT |       239 |          -0.18 |         -42.43 |            -8.471 |          -0.85 |        2:23:00 |   190     0    49  79.5 |
|      BLZ/USDT:USDT |       683 |          -0.07 |         -45.93 |            -9.151 |          -0.92 |        2:15:00 |   529     0   154  77.5 |
|     IOTX/USDT:USDT |       255 |          -0.18 |         -46.16 |            -9.230 |          -0.92 |        3:05:00 |   197     0    58  77.3 |
|      LRC/USDT:USDT |       214 |          -0.43 |         -91.58 |           -18.270 |          -1.83 |        3:22:00 |   162     0    52  75.7 |
|      WOO/USDT:USDT |       160 |          -0.73 |        -116.70 |           -23.292 |          -2.33 |        2:45:00 |   125     0    35  78.1 |
|       AR/USDT:USDT |       177 |          -1.49 |        -264.32 |           -52.560 |          -5.26 |        2:48:00 |   128     0    49  72.3 |
|              TOTAL |     10627 |           0.17 |        1842.62 |           367.438 |          36.74 |        2:57:00 |  8385     0  2242  78.9 |
============================================================= LEFT OPEN TRADES REPORT ==============================================================
|               Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|--------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|     UNFI/USDT:USDT |         1 |          -1.97 |          -1.97 |            -0.391 |          -0.04 |        3:15:00 |     0     0     1     0 |
|    STORJ/USDT:USDT |         1 |          -3.58 |          -3.58 |            -0.714 |          -0.07 |        3:45:00 |     0     0     1     0 |
|      SNX/USDT:USDT |         1 |         -12.00 |         -12.00 |            -2.393 |          -0.24 |        2:40:00 |     0     0     1     0 |
| 1000SHIB/USDT:USDT |         1 |         -14.75 |         -14.75 |            -2.949 |          -0.29 |        5:15:00 |     0     0     1     0 |
|              TOTAL |         4 |          -8.07 |         -32.30 |            -6.447 |          -0.64 |        3:44:00 |     0     0     4     0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     10627 |           0.17 |        1842.62 |           367.438 |          36.74 |        2:57:00 |  8385     0  2242  78.9 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |    8539 |   8229     0   310  96.4 |           3.29 |       28127.8  |          5612.84  |        7031.95 |
|         exit_short |    1548 |      3     0  1545   0.2 |         -12.76 |      -19757.4  |         -3941.61  |       -4939.36 |
|          exit_long |     191 |      0     0   191     0 |         -13.09 |       -2499.85 |          -499.195 |        -624.96 |
|          stop_loss |     190 |      0     0   190     0 |         -31.75 |       -6031.9  |         -1204.34  |       -1507.97 |
|                roi |     155 |    153     0     2  98.7 |          13.14 |        2036.29 |           406.192 |         509.07 |
|         force_exit |       4 |      0     0     4     0 |          -8.07 |         -32.3  |            -6.447 |          -8.07 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2023 |            38.739 |    846 |       0 |      222 |
| 28/02/2023 |            23.972 |    980 |       0 |      238 |
| 31/03/2023 |            94.761 |    954 |       0 |      212 |
| 30/04/2023 |            26.119 |    659 |       0 |      183 |
| 31/05/2023 |            35.947 |    525 |       0 |      149 |
| 30/06/2023 |            13.513 |    693 |       0 |      200 |
| 31/07/2023 |           -10.174 |    571 |       0 |      168 |
| 31/08/2023 |            87.746 |    678 |       0 |      175 |
| 30/09/2023 |           -18.781 |    578 |       0 |      159 |
| 31/10/2023 |            -1.053 |    599 |       0 |      198 |
| 30/11/2023 |            71.276 |    968 |       0 |      232 |
| 31/12/2023 |             5.372 |    334 |       0 |      106 |
=================== SUMMARY METRICS ====================
| Metric                      | Value                  |
|-----------------------------+------------------------|
| Backtesting from            | 2023-01-01 00:00:00    |
| Backtesting to              | 2023-12-12 00:00:00    |
| Max open trades             | 4                      |
|                             |                        |
| Total/Daily Avg Trades      | 10627 / 30.8           |
| Starting balance            | 1000 USDT              |
| Final balance               | 1367.438 USDT          |
| Absolute profit             | 367.438 USDT           |
| Total profit %              | 36.74%                 |
| CAGR %                      | 39.25%                 |
| Sortino                     | 11.13                  |
| Sharpe                      | 12.15                  |
| Calmar                      | 23.00                  |
| Profit factor               | 1.06                   |
| Expectancy (Ratio)          | 0.03 (0.01)            |
| Trades per day              | 30.8                   |
| Avg. daily profit %         | 0.11%                  |
| Avg. stake amount           | 19.956 USDT            |
| Total trade volume          | 212073.521 USDT        |
|                             |                        |
| Long / Short                | 1206 / 9421            |
| Total profit Long %         | 6.09%                  |
| Total profit Short %        | 30.65%                 |
| Absolute profit Long        | 60.919 USDT            |
| Absolute profit Short       | 306.519 USDT           |
|                             |                        |
| Best Pair                   | OGN/USDT:USDT 618.56%  |
| Worst Pair                  | AR/USDT:USDT -264.32%  |
| Best trade                  | STORJ/USDT:USDT 18.85% |
| Worst trade                 | LPT/USDT:USDT -34.68%  |
| Best day                    | 46.183 USDT            |
| Worst day                   | -39.308 USDT           |
| Days win/draw/lose          | 167 / 0 / 179          |
| Avg. Duration Winners       | 2:14:00                |
| Avg. Duration Loser         | 5:36:00                |
| Max Consecutive Wins / Loss | 47 / 10                |
| Rejected Entry signals      | 762864                 |
| Entry/Exit Timeouts         | 0 / 1075               |
|                             |                        |
| Min balance                 | 954.565 USDT           |
| Max balance                 | 1409.97 USDT           |
| Max % of account underwater | 8.85%                  |
| Absolute Drawdown (Account) | 8.85%                  |
| Absolute Drawdown           | 93.53 USDT             |
| Drawdown high               | 57.057 USDT            |
| Drawdown low                | -36.473 USDT           |
| Drawdown Start              | 2023-01-30 23:15:00    |
| Drawdown End                | 2023-02-08 02:05:00    |
| Market change               | 74.01%                 |
========================================================

Backtested 2023-01-01 00:00:00 -> 2023-12-12 00:00:00 | Max open trades : 4
=============================================================================== STRATEGY SUMMARY ==============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |          Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+-------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     10627 |           0.17 |        1842.62 |           367.438 |          36.74 |        2:57:00 |  8385     0  2242  78.9 | 93.53 USDT  8.85% |
===============================================================================================================================================================================















============================================================== BACKTESTING REPORT ==============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| UNFI/USDT:USDT |      4637 |           1.27 |        5895.70 |          1171.434 |         117.14 |        2:18:00 |  3869     0   768  83.4 |
|  CRV/USDT:USDT |      4396 |           1.09 |        4790.14 |           956.821 |          95.68 |        2:12:00 |  3650     0   746  83.0 |
|  LRC/USDT:USDT |      4076 |           0.91 |        3714.39 |           739.114 |          73.91 |        2:43:00 |  3371     0   705  82.7 |
|  CTK/USDT:USDT |      4114 |           0.83 |        3421.68 |           679.116 |          67.91 |        3:03:00 |  3428     0   686  83.3 |
|  RSR/USDT:USDT |      2914 |           0.98 |        2856.32 |           571.013 |          57.10 |        1:49:00 |  2364     0   550  81.1 |
|  C98/USDT:USDT |      1854 |           1.29 |        2389.09 |           472.906 |          47.29 |        2:50:00 |  1552     0   302  83.7 |
|  VET/USDT:USDT |      1989 |           0.98 |        1947.06 |           389.133 |          38.91 |        2:19:00 |  1629     0   360  81.9 |
| BAKE/USDT:USDT |      1068 |           1.44 |        1532.78 |           304.655 |          30.47 |        2:22:00 |   890     0   178  83.3 |
|  IMX/USDT:USDT |      1797 |           0.83 |        1491.81 |           296.744 |          29.67 |        2:41:00 |  1497     0   300  83.3 |
|  ATA/USDT:USDT |      1081 |           1.18 |        1272.66 |           253.917 |          25.39 |        3:34:00 |   903     0   178  83.5 |
|   OP/USDT:USDT |       796 |           1.55 |        1234.63 |           246.705 |          24.67 |        2:12:00 |   650     0   146  81.7 |
| IOTX/USDT:USDT |       963 |           1.09 |        1045.79 |           209.031 |          20.90 |        3:03:00 |   810     0   153  84.1 |
|  LPT/USDT:USDT |       890 |           1.03 |         920.63 |           182.414 |          18.24 |        3:01:00 |   745     1   144  83.7 |
|  WOO/USDT:USDT |      1073 |           0.77 |         830.91 |           165.936 |          16.59 |        3:04:00 |   897     0   176  83.6 |
|  ICP/USDT:USDT |       292 |           1.17 |         342.67 |            66.856 |           6.69 |        4:31:00 |   248     0    44  84.9 |
|          TOTAL |     31940 |           1.05 |       33686.26 |          6705.795 |         670.58 |        2:35:00 | 26503     1  5436  83.0 |
=========================================================== LEFT OPEN TRADES REPORT ============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|  CRV/USDT:USDT |         1 |           0.69 |           0.69 |             0.138 |           0.01 |        0:30:00 |     1     0     0   100 |
| IOTX/USDT:USDT |         1 |           0.18 |           0.18 |             0.036 |           0.00 |        1:00:00 |     1     0     0   100 |
|  LRC/USDT:USDT |         1 |          -2.21 |          -2.21 |            -0.442 |          -0.04 |        0:45:00 |     0     0     1     0 |
|  IMX/USDT:USDT |         1 |          -5.97 |          -5.97 |            -1.192 |          -0.12 |        0:30:00 |     0     0     1     0 |
|          TOTAL |         4 |          -1.83 |          -7.31 |            -1.460 |          -0.15 |        0:41:00 |     2     0     2  50.0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     31940 |           1.05 |       33686.26 |          6705.795 |         670.58 |        2:35:00 | 26503     1  5436  83.0 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   27126 |  25164     0  1962  92.8 |           4.02 |      108975    |         21706.8   |       27243.8  |
|          stop_loss |    2416 |      0     0  2416     0 |         -31.81 |      -76846.2  |        -15306.6   |      -19211.5  |
|                roi |    1356 |   1336     1    19  98.5 |          15.37 |       20837.2  |          4149.26  |        5209.29 |
|         exit_short |     913 |      1     0   912   0.1 |         -18.35 |      -16751.4  |         -3339.78  |       -4187.84 |
|          exit_long |     125 |      0     0   125     0 |         -20.17 |       -2521.19 |          -502.445 |        -630.3  |
|         force_exit |       4 |      2     0     2  50.0 |          -1.83 |          -7.31 |            -1.46  |          -1.83 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |           479.569 |   1218 |       0 |      329 |
| 28/02/2021 |           361.191 |   1074 |       0 |      282 |
| 31/03/2021 |           199.215 |    993 |       0 |      201 |
| 30/04/2021 |           344.018 |    998 |       0 |      236 |
| 31/05/2021 |           699.519 |   1330 |       0 |      333 |
| 30/06/2021 |           282.705 |   1071 |       0 |      210 |
| 31/07/2021 |            90.472 |    817 |       0 |      161 |
| 31/08/2021 |           266.451 |    983 |       0 |      193 |
| 30/09/2021 |           162.756 |    808 |       0 |      168 |
| 31/10/2021 |            48.438 |    750 |       0 |      153 |
| 30/11/2021 |           154.178 |    946 |       0 |      207 |
| 31/12/2021 |           312.83  |    911 |       0 |      162 |
| 31/01/2022 |           172.627 |    796 |       0 |      159 |
| 28/02/2022 |            81.469 |    637 |       0 |      146 |
| 31/03/2022 |            54.597 |    721 |       0 |      147 |
| 30/04/2022 |           158.651 |    594 |       0 |      118 |
| 31/05/2022 |           467.646 |   1405 |       0 |      318 |
| 30/06/2022 |           417.823 |   1230 |       0 |      295 |
| 31/07/2022 |           118.561 |    841 |       0 |      176 |
| 31/08/2022 |           120.84  |    674 |       0 |      113 |
| 30/09/2022 |           135.618 |    491 |       0 |       68 |
| 31/10/2022 |           111.056 |    417 |       0 |       66 |
| 30/11/2022 |           183.864 |    697 |       0 |      146 |
| 31/12/2022 |           107.916 |    328 |       0 |       43 |
| 31/01/2023 |           133.212 |    634 |       0 |      119 |
| 28/02/2023 |           287.781 |    787 |       0 |      118 |
| 31/03/2023 |           246.546 |    732 |       0 |      112 |
| 30/04/2023 |             6.367 |    414 |       0 |       83 |
| 31/05/2023 |            85.277 |    367 |       0 |       53 |
| 30/06/2023 |            54.099 |    407 |       0 |       72 |
| 31/07/2023 |            28.516 |    321 |       0 |       59 |
| 31/08/2023 |           112.609 |    433 |       0 |       79 |
| 30/09/2023 |            21.276 |    353 |       1 |       56 |
| 31/10/2023 |            40.59  |    404 |       0 |       82 |
| 30/11/2023 |           119.469 |    671 |       0 |      118 |
| 31/12/2023 |            38.041 |    250 |       0 |       55 |
==================== SUMMARY METRICS ====================
| Metric                      | Value                   |
|-----------------------------+-------------------------|
| Backtesting from            | 2021-01-01 07:30:00     |
| Backtesting to              | 2023-12-12 00:00:00     |
| Max open trades             | 4                       |
|                             |                         |
| Total/Daily Avg Trades      | 31940 / 29.74           |
| Starting balance            | 1000 USDT               |
| Final balance               | 7705.795 USDT           |
| Absolute profit             | 6705.795 USDT           |
| Total profit %              | 670.58%                 |
| CAGR %                      | 100.16%                 |
| Sortino                     | 45.62                   |
| Sharpe                      | 53.42                   |
| Calmar                      | 524.88                  |
| Profit factor               | 1.32                    |
| Expectancy (Ratio)          | 0.21 (0.06)             |
| Trades per day              | 29.74                   |
| Avg. daily profit %         | 0.62%                   |
| Avg. stake amount           | 19.924 USDT             |
| Total trade volume          | 636375.17 USDT          |
|                             |                         |
| Long / Short                | 3348 / 28592            |
| Total profit Long %         | 77.18%                  |
| Total profit Short %        | 593.39%                 |
| Absolute profit Long        | 771.849 USDT            |
| Absolute profit Short       | 5933.945 USDT           |
|                             |                         |
| Best Pair                   | UNFI/USDT:USDT 5895.70% |
| Worst Pair                  | ICP/USDT:USDT 342.67%   |
| Best trade                  | CRV/USDT:USDT 19.82%    |
| Worst trade                 | UNFI/USDT:USDT -39.65%  |
| Best day                    | 107.604 USDT            |
| Worst day                   | -51.546 USDT            |
| Days win/draw/lose          | 647 / 2 / 427           |
| Avg. Duration Winners       | 1:59:00                 |
| Avg. Duration Loser         | 5:26:00                 |
| Max Consecutive Wins / Loss | 72 / 10                 |
| Rejected Entry signals      | 271904                  |
| Entry/Exit Timeouts         | 0 / 11233               |
|                             |                         |
| Min balance                 | 976.461 USDT            |
| Max balance                 | 7711.658 USDT           |
| Max % of account underwater | 6.52%                   |
| Absolute Drawdown (Account) | 2.27%                   |
| Absolute Drawdown           | 108.495 USDT            |
| Drawdown high               | 3774.007 USDT           |
| Drawdown low                | 3665.511 USDT           |
| Drawdown Start              | 2022-03-15 16:00:00     |
| Drawdown End                | 2022-03-28 08:00:00     |
| Market change               | -36.56%                 |
=========================================================

Backtested 2021-01-01 07:30:00 -> 2023-12-12 00:00:00 | Max open trades : 4
================================================================================ STRATEGY SUMMARY ===============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |            Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+---------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     31940 |           1.05 |       33686.26 |          6705.795 |         670.58 |        2:35:00 | 26503     1  5436  83.0 | 108.495 USDT  2.27% |
=================================================================================================================================================================================







============================================================== BACKTESTING REPORT ==============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| UNFI/USDT:USDT |      3277 |           1.36 |        4463.15 |           885.562 |          88.56 |        2:03:00 |  2717     0   560  82.9 |
|  CRV/USDT:USDT |      3211 |           1.14 |        3665.21 |           732.051 |          73.21 |        1:51:00 |  2631     0   580  81.9 |
|  C98/USDT:USDT |      2835 |           1.25 |        3557.49 |           704.767 |          70.48 |        2:50:00 |  2383     0   452  84.1 |
|  RSR/USDT:USDT |      3457 |           1.02 |        3521.25 |           703.966 |          70.40 |        1:50:00 |  2826     0   631  81.7 |
| BAKE/USDT:USDT |      3900 |           0.82 |        3187.53 |           634.186 |          63.42 |        2:51:00 |  3239     0   661  83.1 |
|  LPT/USDT:USDT |      2487 |           1.25 |        3105.51 |           616.179 |          61.62 |        3:22:00 |  2126     1   360  85.5 |
|  VET/USDT:USDT |      2986 |           1.00 |        2992.94 |           598.130 |          59.81 |        2:31:00 |  2463     0   523  82.5 |
| IOTX/USDT:USDT |      2301 |           1.12 |        2578.81 |           515.516 |          51.55 |        3:16:00 |  1944     0   357  84.5 |
|  CTK/USDT:USDT |      2592 |           0.96 |        2492.94 |           494.323 |          49.43 |        2:18:00 |  2136     0   456  82.4 |
|  LRC/USDT:USDT |      2558 |           0.89 |        2275.36 |           453.040 |          45.30 |        2:15:00 |  2099     0   459  82.1 |
|  ATA/USDT:USDT |      2334 |           0.91 |        2127.58 |           424.736 |          42.47 |        3:18:00 |  1943     0   391  83.2 |
|   OP/USDT:USDT |      1140 |           1.22 |        1393.92 |           278.519 |          27.85 |        2:23:00 |   940     0   200  82.5 |
|  IMX/USDT:USDT |      1511 |           0.79 |        1191.98 |           237.258 |          23.73 |        2:36:00 |  1252     0   259  82.9 |
|  WOO/USDT:USDT |      2208 |           0.53 |        1176.29 |           234.864 |          23.49 |        3:07:00 |  1859     0   349  84.2 |
|  ICP/USDT:USDT |       941 |           1.19 |        1122.78 |           218.043 |          21.80 |        5:02:00 |   796     0   145  84.6 |
|          TOTAL |     37738 |           1.03 |       38852.72 |          7731.139 |         773.11 |        2:38:00 | 31354     1  6383  83.1 |
=========================================================== LEFT OPEN TRADES REPORT ============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| IOTX/USDT:USDT |         1 |           0.18 |           0.18 |             0.036 |           0.00 |        1:00:00 |     1     0     0   100 |
|  LRC/USDT:USDT |         1 |          -2.21 |          -2.21 |            -0.442 |          -0.04 |        0:45:00 |     0     0     1     0 |
|   OP/USDT:USDT |         1 |          -2.27 |          -2.27 |            -0.454 |          -0.05 |        0:30:00 |     0     0     1     0 |
|          TOTAL |         3 |          -1.44 |          -4.31 |            -0.860 |          -0.09 |        0:45:00 |     1     0     2  33.3 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     37738 |           1.03 |       38852.72 |          7731.139 |         773.11 |        2:38:00 | 31354     1  6383  83.1 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   32042 |  29823     0  2219  93.1 |           4    |      128181    |         25528.1   |       25636.2  |
|          stop_loss |    2762 |      0     0  2762     0 |         -31.81 |      -87858.1  |        -17499.5   |      -17571.6  |
|                roi |    1561 |   1529     1    31  98.0 |          15.03 |       23460.7  |          4670.61  |        4692.14 |
|         exit_short |    1199 |      1     0  1198   0.1 |         -17.89 |      -21455.8  |         -4275.3   |       -4291.16 |
|          exit_long |     171 |      0     0   171     0 |         -20.3  |       -3470.68 |          -691.865 |        -694.14 |
|         force_exit |       3 |      1     0     2  33.3 |          -1.44 |          -4.31 |            -0.86  |          -0.86 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |           462.494 |   1262 |       0 |      351 |
| 28/02/2021 |           402.728 |   1136 |       0 |      296 |
| 31/03/2021 |           221.08  |   1108 |       0 |      221 |
| 30/04/2021 |           348.593 |   1114 |       0 |      282 |
| 31/05/2021 |           775.426 |   1539 |       0 |      385 |
| 30/06/2021 |           363.601 |   1248 |       0 |      245 |
| 31/07/2021 |           107.181 |    943 |       0 |      195 |
| 31/08/2021 |           394.246 |   1159 |       0 |      209 |
| 30/09/2021 |           298.063 |   1032 |       0 |      201 |
| 31/10/2021 |            74.858 |    857 |       0 |      174 |
| 30/11/2021 |           288.073 |   1096 |       0 |      217 |
| 31/12/2021 |           324.431 |   1008 |       0 |      171 |
| 31/01/2022 |           156.101 |    897 |       0 |      169 |
| 28/02/2022 |            40.78  |    787 |       0 |      178 |
| 31/03/2022 |           104.581 |    854 |       0 |      165 |
| 30/04/2022 |           190.168 |    736 |       0 |      141 |
| 31/05/2022 |           604.38  |   1658 |       0 |      378 |
| 30/06/2022 |           473.402 |   1549 |       0 |      351 |
| 31/07/2022 |            78.744 |    997 |       0 |      205 |
| 31/08/2022 |            88.291 |    766 |       0 |      135 |
| 30/09/2022 |           118.348 |    536 |       0 |       81 |
| 31/10/2022 |            98.551 |    489 |       0 |       81 |
| 30/11/2022 |           166.278 |    831 |       0 |      180 |
| 31/12/2022 |            94.227 |    371 |       0 |       57 |
| 31/01/2023 |            52.364 |    744 |       0 |      154 |
| 28/02/2023 |           267.128 |    939 |       0 |      153 |
| 31/03/2023 |           295.614 |    888 |       0 |      143 |
| 30/04/2023 |            86.019 |    591 |       0 |      110 |
| 31/05/2023 |            74.379 |    463 |       0 |       78 |
| 30/06/2023 |            73.911 |    562 |       0 |      104 |
| 31/07/2023 |           126.082 |    438 |       0 |       60 |
| 31/08/2023 |           101.308 |    623 |       0 |      115 |
| 30/09/2023 |            74.656 |    449 |       1 |       70 |
| 31/10/2023 |            60.737 |    525 |       0 |      116 |
| 30/11/2023 |           180.495 |    831 |       0 |      144 |
| 31/12/2023 |            63.82  |    328 |       0 |       68 |
==================== SUMMARY METRICS ====================
| Metric                      | Value                   |
|-----------------------------+-------------------------|
| Backtesting from            | 2021-01-01 07:30:00     |
| Backtesting to              | 2023-12-12 00:00:00     |
| Max open trades             | 5                       |
|                             |                         |
| Total/Daily Avg Trades      | 37738 / 35.14           |
| Starting balance            | 1000 USDT               |
| Final balance               | 8731.139 USDT           |
| Absolute profit             | 7731.139 USDT           |
| Total profit %              | 773.11%                 |
| CAGR %                      | 108.84%                 |
| Sortino                     | 53.15                   |
| Sharpe                      | 62.25                   |
| Calmar                      | 528.09                  |
| Profit factor               | 1.32                    |
| Expectancy (Ratio)          | 0.20 (0.05)             |
| Trades per day              | 35.14                   |
| Avg. daily profit %         | 0.72%                   |
| Avg. stake amount           | 19.919 USDT             |
| Total trade volume          | 751710.471 USDT         |
|                             |                         |
| Long / Short                | 4339 / 33399            |
| Total profit Long %         | 85.01%                  |
| Total profit Short %        | 688.10%                 |
| Absolute profit Long        | 850.114 USDT            |
| Absolute profit Short       | 6881.025 USDT           |
|                             |                         |
| Best Pair                   | UNFI/USDT:USDT 4463.15% |
| Worst Pair                  | ICP/USDT:USDT 1122.78%  |
| Best trade                  | CRV/USDT:USDT 19.82%    |
| Worst trade                 | LPT/USDT:USDT -36.27%   |
| Best day                    | 131.99 USDT             |
| Worst day                   | -61.989 USDT            |
| Days win/draw/lose          | 654 / 3 / 419           |
| Avg. Duration Winners       | 2:01:00                 |
| Avg. Duration Loser         | 5:36:00                 |
| Max Consecutive Wins / Loss | 102 / 12                |
| Rejected Entry signals      | 223850                  |
| Entry/Exit Timeouts         | 0 / 13137               |
|                             |                         |
| Min balance                 | 976.257 USDT            |
| Max balance                 | 8737.172 USDT           |
| Max % of account underwater | 6.67%                   |
| Absolute Drawdown (Account) | 2.60%                   |
| Absolute Drawdown           | 142.015 USDT            |
| Drawdown high               | 4453.322 USDT           |
| Drawdown low                | 4311.306 USDT           |
| Drawdown Start              | 2022-03-15 13:30:00     |
| Drawdown End                | 2022-03-28 10:30:00     |
| Market change               | -36.56%                 |
=========================================================

Backtested 2021-01-01 07:30:00 -> 2023-12-12 00:00:00 | Max open trades : 5
================================================================================ STRATEGY SUMMARY ===============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |            Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+---------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     37738 |           1.03 |       38852.72 |          7731.139 |         773.11 |        2:38:00 | 31354     1  6383  83.1 | 142.015 USDT  2.60% |
=================================================================================================================================================================================







============================================================== BACKTESTING REPORT ==============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| UNFI/USDT:USDT |      4955 |           1.21 |        5976.04 |          1187.344 |         118.73 |        2:22:00 |  4120     0   835  83.1 |
|  CRV/USDT:USDT |      4150 |           1.10 |        4569.70 |           912.806 |          91.28 |        2:01:00 |  3428     0   722  82.6 |
|  LRC/USDT:USDT |      4704 |           0.89 |        4210.04 |           838.634 |          83.86 |        2:50:00 |  3906     0   798  83.0 |
|  RSR/USDT:USDT |      3758 |           1.05 |        3941.96 |           788.085 |          78.81 |        1:56:00 |  3080     0   678  82.0 |
|  VET/USDT:USDT |      4141 |           0.83 |        3429.62 |           685.386 |          68.54 |        3:04:00 |  3436     0   705  83.0 |
|  LPT/USDT:USDT |      2608 |           1.20 |        3140.20 |           622.747 |          62.27 |        3:23:00 |  2226     0   382  85.4 |
| IOTX/USDT:USDT |      2938 |           0.95 |        2801.36 |           559.978 |          56.00 |        3:22:00 |  2479     0   459  84.4 |
|  CTK/USDT:USDT |      3812 |           0.70 |        2675.49 |           530.429 |          53.04 |        2:45:00 |  3144     0   668  82.5 |
|  ATA/USDT:USDT |      2663 |           0.88 |        2350.55 |           468.962 |          46.90 |        3:21:00 |  2218     0   445  83.3 |
| BAKE/USDT:USDT |      2336 |           0.89 |        2079.21 |           413.706 |          41.37 |        2:35:00 |  1930     0   406  82.6 |
|  C98/USDT:USDT |      1358 |           1.36 |        1846.02 |           364.967 |          36.50 |        2:43:00 |  1139     0   219  83.9 |
|   OP/USDT:USDT |      1313 |           1.30 |        1702.43 |           340.169 |          34.02 |        2:27:00 |  1081     0   232  82.3 |
|  WOO/USDT:USDT |      1717 |           0.43 |         741.38 |           148.025 |          14.80 |        3:00:00 |  1429     0   288  83.2 |
|  IMX/USDT:USDT |      1181 |           0.60 |         711.74 |           141.913 |          14.19 |        2:48:00 |   967     0   214  81.9 |
|  ICP/USDT:USDT |       437 |           1.09 |         477.62 |            93.770 |           9.38 |        4:30:00 |   369     0    68  84.4 |
|          TOTAL |     42071 |           0.97 |       40653.34 |          8096.920 |         809.69 |        2:44:00 | 34952     0  7119  83.1 |
=========================================================== LEFT OPEN TRADES REPORT ============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| IOTX/USDT:USDT |         1 |           0.18 |           0.18 |             0.036 |           0.00 |        1:00:00 |     1     0     0   100 |
|  LRC/USDT:USDT |         1 |          -2.21 |          -2.21 |            -0.442 |          -0.04 |        0:45:00 |     0     0     1     0 |
|  VET/USDT:USDT |         1 |          -2.55 |          -2.55 |            -0.510 |          -0.05 |        0:30:00 |     0     0     1     0 |
|  CTK/USDT:USDT |         1 |         -26.00 |         -26.00 |            -5.178 |          -0.52 |        5:15:00 |     0     0     1     0 |
|          TOTAL |         4 |          -7.65 |         -30.59 |            -6.095 |          -0.61 |        1:52:00 |     1     0     3  25.0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     42071 |           0.97 |       40653.34 |          8096.920 |         809.69 |        2:44:00 | 34952     0  7119  83.1 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   35703 |  33269     0  2434  93.2 |           3.97 |      141679    |         28229.6   |       23613.2  |
|          stop_loss |    3074 |      0     0  3074     0 |         -31.81 |      -97794.5  |        -19481.8   |      -16299.1  |
|                roi |    1723 |   1680     0    43  97.5 |          14.68 |       25301.6  |          5038.62  |        4216.93 |
|         exit_short |    1350 |      2     0  1348   0.1 |         -17.89 |      -24146    |         -4814.62  |       -4024.34 |
|          exit_long |     217 |      0     0   217     0 |         -20.07 |       -4356.03 |          -868.816 |        -726    |
|         force_exit |       4 |      1     0     3  25.0 |          -7.65 |         -30.59 |            -6.095 |          -5.1  |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |           462.494 |   1262 |       0 |      351 |
| 28/02/2021 |           404.273 |   1148 |       0 |      306 |
| 31/03/2021 |           230.09  |   1142 |       0 |      228 |
| 30/04/2021 |           379.908 |   1145 |       0 |      291 |
| 31/05/2021 |           775.164 |   1608 |       0 |      407 |
| 30/06/2021 |           364.091 |   1355 |       0 |      267 |
| 31/07/2021 |           114.732 |   1042 |       0 |      217 |
| 31/08/2021 |           308.607 |   1282 |       0 |      240 |
| 30/09/2021 |           307.954 |   1193 |       0 |      223 |
| 31/10/2021 |           114.09  |   1020 |       0 |      197 |
| 30/11/2021 |           341.129 |   1382 |       0 |      286 |
| 31/12/2021 |           354.05  |   1199 |       0 |      214 |
| 31/01/2022 |           197.204 |   1051 |       0 |      196 |
| 28/02/2022 |            12.18  |    888 |       0 |      190 |
| 31/03/2022 |            61.532 |    990 |       0 |      206 |
| 30/04/2022 |           197.89  |    794 |       0 |      149 |
| 31/05/2022 |           632.825 |   1877 |       0 |      407 |
| 30/06/2022 |           547.609 |   1744 |       0 |      432 |
| 31/07/2022 |           126.43  |   1169 |       0 |      238 |
| 31/08/2022 |            59.219 |    861 |       0 |      155 |
| 30/09/2022 |           141.393 |    646 |       0 |       97 |
| 31/10/2022 |           134.972 |    571 |       0 |       95 |
| 30/11/2022 |           218.106 |    921 |       0 |      190 |
| 31/12/2022 |           157.074 |    473 |       0 |       59 |
| 31/01/2023 |            80.863 |    844 |       0 |      168 |
| 28/02/2023 |           315.334 |   1073 |       0 |      178 |
| 31/03/2023 |           339.057 |   1038 |       0 |      160 |
| 30/04/2023 |            53.815 |    592 |       0 |      119 |
| 31/05/2023 |            77.124 |    496 |       0 |       83 |
| 30/06/2023 |            85.08  |    597 |       0 |       98 |
| 31/07/2023 |            82.206 |    467 |       0 |       78 |
| 31/08/2023 |            96.271 |    647 |       0 |      137 |
| 30/09/2023 |            81.912 |    542 |       0 |       86 |
| 31/10/2023 |            61.148 |    626 |       0 |      124 |
| 30/11/2023 |           157.481 |    905 |       0 |      164 |
| 31/12/2023 |            23.615 |    362 |       0 |       83 |
==================== SUMMARY METRICS ====================
| Metric                      | Value                   |
|-----------------------------+-------------------------|
| Backtesting from            | 2021-01-01 07:30:00     |
| Backtesting to              | 2023-12-12 00:00:00     |
| Max open trades             | 6                       |
|                             |                         |
| Total/Daily Avg Trades      | 42071 / 39.17           |
| Starting balance            | 1000 USDT               |
| Final balance               | 9096.92 USDT            |
| Absolute profit             | 8096.92 USDT            |
| Total profit %              | 809.69%                 |
| CAGR %                      | 111.78%                 |
| Sortino                     | 55.75                   |
| Sharpe                      | 65.28                   |
| Calmar                      | 466.45                  |
| Profit factor               | 1.30                    |
| Expectancy (Ratio)          | 0.19 (0.05)             |
| Trades per day              | 39.17                   |
| Avg. daily profit %         | 0.75%                   |
| Avg. stake amount           | 19.929 USDT             |
| Total trade volume          | 838431.987 USDT         |
|                             |                         |
| Long / Short                | 5097 / 36974            |
| Total profit Long %         | 88.74%                  |
| Total profit Short %        | 720.95%                 |
| Absolute profit Long        | 887.447 USDT            |
| Absolute profit Short       | 7209.473 USDT           |
|                             |                         |
| Best Pair                   | UNFI/USDT:USDT 5976.04% |
| Worst Pair                  | ICP/USDT:USDT 477.62%   |
| Best trade                  | CRV/USDT:USDT 19.82%    |
| Worst trade                 | UNFI/USDT:USDT -39.65%  |
| Best day                    | 143.556 USDT            |
| Worst day                   | -73.098 USDT            |
| Days win/draw/lose          | 659 / 0 / 417           |
| Avg. Duration Winners       | 2:05:00                 |
| Avg. Duration Loser         | 5:57:00                 |
| Max Consecutive Wins / Loss | 69 / 12                 |
| Rejected Entry signals      | 179939                  |
| Entry/Exit Timeouts         | 0 / 14404               |
|                             |                         |
| Min balance                 | 976.257 USDT            |
| Max balance                 | 9105.818 USDT           |
| Max % of account underwater | 6.64%                   |
| Absolute Drawdown (Account) | 3.09%                   |
| Absolute Drawdown           | 171.534 USDT            |
| Drawdown high               | 4555.104 USDT           |
| Drawdown low                | 4383.569 USDT           |
| Drawdown Start              | 2022-03-14 03:00:00     |
| Drawdown End                | 2022-03-28 10:30:00     |
| Market change               | -36.56%                 |
=========================================================

Backtested 2021-01-01 07:30:00 -> 2023-12-12 00:00:00 | Max open trades : 6
================================================================================ STRATEGY SUMMARY ===============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |            Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+---------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     42071 |           0.97 |       40653.34 |          8096.920 |         809.69 |        2:44:00 | 34952     0  7119  83.1 | 171.534 USDT  3.09% |
=================================================================================================================================================================================



Result for strategy RSI_BB_MACD_Dec_2023_15m_3_rls
============================================================== BACKTESTING REPORT ==============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|  CRV/USDT:USDT |      5842 |           1.03 |        6038.75 |          1206.308 |         120.63 |        2:27:00 |  4852     0   990  83.1 |
| UNFI/USDT:USDT |      5474 |           1.10 |        6000.69 |          1191.695 |         119.17 |        2:27:00 |  4533     0   941  82.8 |
|  RSR/USDT:USDT |      5820 |           1.00 |        5790.98 |          1157.822 |         115.78 |        2:26:00 |  4838     0   982  83.1 |
|  LRC/USDT:USDT |      5116 |           0.96 |        4928.66 |           981.111 |          98.11 |        2:58:00 |  4256     0   860  83.2 |
|  C98/USDT:USDT |      3822 |           1.23 |        4696.22 |           930.130 |          93.01 |        3:08:00 |  3251     0   571  85.1 |
| BAKE/USDT:USDT |      4403 |           0.85 |        3752.70 |           747.104 |          74.71 |        2:59:00 |  3674     0   729  83.4 |
|  CTK/USDT:USDT |      4842 |           0.75 |        3620.70 |           718.420 |          71.84 |        3:12:00 |  4047     0   795  83.6 |
|  VET/USDT:USDT |      4845 |           0.73 |        3559.60 |           711.363 |          71.14 |        3:17:00 |  4019     0   826  83.0 |
| IOTX/USDT:USDT |      3597 |           0.91 |        3291.24 |           657.905 |          65.79 |        3:26:00 |  3022     0   575  84.0 |
|  LPT/USDT:USDT |      3142 |           1.03 |        3225.50 |           640.402 |          64.04 |        3:32:00 |  2669     2   471  84.9 |
|   OP/USDT:USDT |      2702 |           1.14 |        3076.78 |           614.783 |          61.48 |        2:45:00 |  2242     0   460  83.0 |
|  IMX/USDT:USDT |      3279 |           0.78 |        2552.31 |           507.936 |          50.79 |        2:52:00 |  2736     0   543  83.4 |
|  ATA/USDT:USDT |      3390 |           0.72 |        2450.66 |           488.649 |          48.86 |        3:32:00 |  2825     0   565  83.3 |
|  WOO/USDT:USDT |      2748 |           0.58 |        1582.63 |           316.084 |          31.61 |        3:11:00 |  2317     0   431  84.3 |
|  ICP/USDT:USDT |      1310 |           1.03 |        1350.81 |           263.523 |          26.35 |        5:17:00 |  1111     0   199  84.8 |
|          TOTAL |     60332 |           0.93 |       55918.23 |         11133.236 |        1113.32 |        3:01:00 | 50392     2  9938  83.5 |
=========================================================== LEFT OPEN TRADES REPORT ============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|  CRV/USDT:USDT |         1 |           0.69 |           0.69 |             0.138 |           0.01 |        0:30:00 |     1     0     0   100 |
| IOTX/USDT:USDT |         1 |           0.18 |           0.18 |             0.036 |           0.00 |        1:00:00 |     1     0     0   100 |
|  LRC/USDT:USDT |         1 |          -2.21 |          -2.21 |            -0.442 |          -0.04 |        0:45:00 |     0     0     1     0 |
|   OP/USDT:USDT |         1 |          -2.27 |          -2.27 |            -0.454 |          -0.05 |        0:30:00 |     0     0     1     0 |
|  VET/USDT:USDT |         1 |          -2.55 |          -2.55 |            -0.510 |          -0.05 |        0:30:00 |     0     0     1     0 |
|          TOTAL |         5 |          -1.23 |          -6.17 |            -1.233 |          -0.12 |        0:39:00 |     2     0     3  40.0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     60332 |           0.93 |       55918.23 |         11133.236 |        1113.32 |        3:01:00 | 50392     2  9938  83.5 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   51325 |  48181     0  3144  93.9 |           3.93 |      201509    |         40150.3   |       13434    |
|          stop_loss |    4158 |      0     0  4158     0 |         -31.82 |     -132321    |        -26364.9   |       -8821.43 |
|                roi |    2306 |   2209     2    95  95.8 |          13.93 |       32125.7  |          6398.36  |        2141.72 |
|         exit_short |    1995 |      0     0  1995     0 |         -17.76 |      -35433.4  |         -7063.42  |       -2362.23 |
|          exit_long |     543 |      0     0   543     0 |         -18.33 |       -9955.81 |         -1985.91  |        -663.72 |
|         force_exit |       5 |      2     0     3  40.0 |          -1.23 |          -6.17 |            -1.233 |          -0.41 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |           462.494 |   1262 |       0 |      351 |
| 28/02/2021 |           404.273 |   1148 |       0 |      306 |
| 31/03/2021 |           230.09  |   1142 |       0 |      228 |
| 30/04/2021 |           379.908 |   1145 |       0 |      291 |
| 31/05/2021 |           796.157 |   1622 |       0 |      410 |
| 30/06/2021 |           380.04  |   1409 |       0 |      275 |
| 31/07/2021 |           146.536 |   1104 |       0 |      225 |
| 31/08/2021 |           440.782 |   1431 |       0 |      252 |
| 30/09/2021 |           370.968 |   1522 |       0 |      284 |
| 31/10/2021 |           207.048 |   1268 |       0 |      244 |
| 30/11/2021 |           449.42  |   1713 |       0 |      343 |
| 31/12/2021 |           493.033 |   1628 |       0 |      285 |
| 31/01/2022 |           140.227 |   1321 |       0 |      263 |
| 28/02/2022 |            -3.363 |   1223 |       0 |      274 |
| 31/03/2022 |           238.596 |   1552 |       0 |      301 |
| 30/04/2022 |           382.055 |   1311 |       0 |      221 |
| 31/05/2022 |           891.303 |   2808 |       0 |      608 |
| 30/06/2022 |           924.276 |   2800 |       0 |      642 |
| 31/07/2022 |           216.476 |   1805 |       0 |      365 |
| 31/08/2022 |           193.812 |   1532 |       0 |      260 |
| 30/09/2022 |           247.407 |   1232 |       0 |      193 |
| 31/10/2022 |           276.632 |   1132 |       0 |      190 |
| 30/11/2022 |           405.743 |   1596 |       0 |      310 |
| 31/12/2022 |           247.09  |    890 |       0 |      136 |
| 31/01/2023 |           216.025 |   1536 |       0 |      285 |
| 28/02/2023 |           509.142 |   1724 |       0 |      277 |
| 31/03/2023 |           473.457 |   1777 |       0 |      274 |
| 30/04/2023 |           144.859 |   1197 |       0 |      224 |
| 31/05/2023 |            97.261 |    952 |       0 |      166 |
| 30/06/2023 |            42.403 |   1012 |       0 |      194 |
| 31/07/2023 |           181.408 |   1029 |       0 |      157 |
| 31/08/2023 |           121.32  |   1161 |       0 |      251 |
| 30/09/2023 |            98.841 |    999 |       2 |      175 |
| 31/10/2023 |            -7.92  |   1092 |       0 |      259 |
| 30/11/2023 |           219.044 |   1703 |       0 |      295 |
| 31/12/2023 |           116.391 |    614 |       0 |      124 |
=================== SUMMARY METRICS ====================
| Metric                      | Value                  |
|-----------------------------+------------------------|
| Backtesting from            | 2021-01-01 07:30:00    |
| Backtesting to              | 2023-12-12 00:00:00    |
| Max open trades             | 15                     |
|                             |                        |
| Total/Daily Avg Trades      | 60332 / 56.18          |
| Starting balance            | 1000 USDT              |
| Final balance               | 12133.236 USDT         |
| Absolute profit             | 11133.236 USDT         |
| Total profit %              | 1113.32%               |
| CAGR %                      | 133.56%                |
| Sortino                     | 77.47                  |
| Sharpe                      | 91.77                  |
| Calmar                      | 798.68                 |
| Profit factor               | 1.30                   |
| Expectancy (Ratio)          | 0.18 (0.05)            |
| Trades per day              | 56.18                  |
| Avg. daily profit %         | 1.04%                  |
| Avg. stake amount           | 19.929 USDT            |
| Total trade volume          | 1202351.08 USDT        |
|                             |                        |
| Long / Short                | 9598 / 50734           |
| Total profit Long %         | 129.22%                |
| Total profit Short %        | 984.11%                |
| Absolute profit Long        | 1292.173 USDT          |
| Absolute profit Short       | 9841.063 USDT          |
|                             |                        |
| Best Pair                   | CRV/USDT:USDT 6038.75% |
| Worst Pair                  | ICP/USDT:USDT 1350.81% |
| Best trade                  | ATA/USDT:USDT 22.16%   |
| Worst trade                 | UNFI/USDT:USDT -47.62% |
| Best day                    | 212.244 USDT           |
| Worst day                   | -119.288 USDT          |
| Days win/draw/lose          | 691 / 0 / 385          |
| Avg. Duration Winners       | 2:16:00                |
| Avg. Duration Loser         | 6:44:00                |
| Max Consecutive Wins / Loss | 81 / 13                |
| Rejected Entry signals      | 0                      |
| Entry/Exit Timeouts         | 0 / 19235              |
|                             |                        |
| Min balance                 | 976.257 USDT           |
| Max balance                 | 12140.2 USDT           |
| Max % of account underwater | 6.64%                  |
| Absolute Drawdown (Account) | 2.48%                  |
| Absolute Drawdown           | 202.663 USDT           |
| Drawdown high               | 7173.045 USDT          |
| Drawdown low                | 6970.383 USDT          |
| Drawdown Start              | 2022-06-19 08:15:00    |
| Drawdown End                | 2022-06-21 13:45:00    |
| Market change               | -36.56%                |
========================================================

Backtested 2021-01-01 07:30:00 -> 2023-12-12 00:00:00 | Max open trades : 15
================================================================================ STRATEGY SUMMARY ===============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |            Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+---------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     60332 |           0.93 |       55918.23 |         11133.236 |        1113.32 |        3:01:00 | 50392     2  9938  83.5 | 202.663 USDT  2.48% |
=================================================================================================================================================================================



 sudo docker compose run freqtrade backtesting --strategy RSI_BB_MACD_Dec_2023_15m_3_rls -i 15m --export trades --breakdown month --timerange 2
0210101-20231212 --enable-protections
[sudo] password for picasso999:
2023-12-19 15:20:57,610 - freqtrade - INFO - freqtrade 2023.10
2023-12-19 15:20:57,648 - freqtrade.configuration.load_config - INFO - Using config: user_data/config.json ...
2023-12-19 15:20:57,650 - freqtrade.loggers - INFO - Verbosity set to 0
2023-12-19 15:20:57,651 - freqtrade.configuration.configuration - INFO - Parameter -i/--timeframe detected ... Using timeframe: 15m ...
2023-12-19 15:20:57,651 - freqtrade.configuration.configuration - INFO - Parameter --enable-protections detected, enabling Protections. ...
2023-12-19 15:20:57,651 - freqtrade.configuration.configuration - INFO - Using max_open_trades: 5 ...
2023-12-19 15:20:57,651 - freqtrade.configuration.configuration - INFO - Parameter --timerange detected: 20210101-20231212 ...
2023-12-19 15:20:57,758 - freqtrade.configuration.configuration - INFO - Using user-data directory: /freqtrade/user_data ...
2023-12-19 15:20:57,759 - freqtrade.configuration.configuration - INFO - Using data directory: /freqtrade/user_data/data/binance ...
2023-12-19 15:20:57,759 - freqtrade.configuration.configuration - INFO - Overriding timeframe with Command line argument
2023-12-19 15:20:57,759 - freqtrade.configuration.configuration - INFO - Parameter --export detected: trades ...
2023-12-19 15:20:57,759 - freqtrade.configuration.configuration - INFO - Parameter --breakdown detected ...
2023-12-19 15:20:57,759 - freqtrade.configuration.configuration - INFO - Parameter --cache=day detected ...
2023-12-19 15:20:57,759 - freqtrade.configuration.configuration - INFO - Filter trades by timerange: 20210101-20231212
2023-12-19 15:20:57,761 - freqtrade.exchange.check_exchange - INFO - Checking exchange...
2023-12-19 15:20:57,789 - freqtrade.exchange.check_exchange - INFO - Exchange "binance" is officially supported by the Freqtrade development team.
2023-12-19 15:20:57,789 - freqtrade.configuration.configuration - INFO - Using pairlist from configuration.
2023-12-19 15:20:57,789 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2023-12-19 15:20:57,801 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2023-12-19 15:20:57,802 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2023-12-19 15:20:57,802 - freqtrade.exchange.exchange - INFO - Using CCXT 4.1.22
2023-12-19 15:20:57,802 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}, 'enableRateLimit': True}
2023-12-19 15:20:57,828 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}, 'enableRateLimit': True, 'rateLimit': 50}
2023-12-19 15:20:57,855 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2023-12-19 15:21:05,455 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2023-12-19 15:21:06,811 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy RSI_BB_MACD_Dec_2023_15m_3_rls from '/freqtrade/user_data/strategies/RSI_BB_MACD_Dec_2023_15m_3_rls.py'...
2023-12-19 15:21:06,811 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2023-12-19 15:21:06,812 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 15m.
2023-12-19 15:21:06,812 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 20.
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'entry': 10, 'exit': 10, 'exit_timeout_count': 0, 'unit': 'minutes'}.
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'max_open_trades' with value in config file: 5.
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.184, '416': 0.14, '933': 0.073, '1982': 0}
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 15m
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.317
2023-12-19 15:21:06,813 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: True
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive: 0.012
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.03
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: True
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: False
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: True
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'entry': 'GTC', 'exit': 'GTC'}
2023-12-19 15:21:06,814 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 20
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using protections: [{'method': 'MaxDrawdown', 'lookback_period_candles': 2, 'trade_limit': 1, 'stop_duration_candles': 4, 'max_allowed_drawdown': 0.1}, {'method': 'StoplossGuard', 'lookback_period_candles': 8, 'trade_limit': 1, 'stop_duration_candles': 4, 'only_per_pair': False}]
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using startup_candle_count: 30
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using unfilledtimeout: {'entry': 10, 'exit': 10, 'exit_timeout_count': 0, 'unit': 'minutes'}
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_exit_signal: True
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_only: False
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2023-12-19 15:21:06,815 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2023-12-19 15:21:06,816 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2023-12-19 15:21:06,816 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2023-12-19 15:21:06,816 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2023-12-19 15:21:06,816 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2023-12-19 15:21:06,816 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 5
2023-12-19 15:21:06,816 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2023-12-19 15:21:06,863 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist StaticPairList from '/freqtrade/freqtrade/plugins/pairlist/StaticPairList.py'...
2023-12-19 15:21:06,922 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist AgeFilter from '/freqtrade/freqtrade/plugins/pairlist/AgeFilter.py'...
2023-12-19 15:21:06,941 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist VolatilityFilter from '/freqtrade/freqtrade/plugins/pairlist/VolatilityFilter.py'...
2023-12-19 15:21:06,950 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist RangeStabilityFilter from '/freqtrade/freqtrade/plugins/pairlist/rangestabilityfilter.py'...
2023-12-19 15:21:06,975 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist ShuffleFilter from '/freqtrade/freqtrade/plugins/pairlist/ShuffleFilter.py'...
2023-12-19 15:21:06,975 - ShuffleFilter - INFO - Backtesting mode detected, applying seed value: None
2023-12-19 15:22:24,001 - freqtrade.data.history.history_utils - INFO - Using indicator startup period: 30 ...
2023-12-19 15:22:24,069 - freqtrade.data.history.idatahandler - WARNING - ATA/USDT:USDT, futures, 15m, data starts at 2021-08-31 03:30:00
2023-12-19 15:22:24,184 - freqtrade.data.history.idatahandler - WARNING - IMX/USDT:USDT, futures, 15m, data starts at 2022-02-11 03:30:00
2023-12-19 15:22:24,286 - freqtrade.data.history.idatahandler - WARNING - OP/USDT:USDT, futures, 15m, data starts at 2022-06-01 14:00:00
2023-12-19 15:22:24,389 - freqtrade.data.history.idatahandler - WARNING - IOTX/USDT:USDT, futures, 15m, data starts at 2021-08-12 03:30:00
2023-12-19 15:22:24,520 - freqtrade.data.history.idatahandler - WARNING - WOO/USDT:USDT, futures, 15m, data starts at 2022-04-08 03:30:00
2023-12-19 15:22:24,635 - freqtrade.data.history.idatahandler - WARNING - CTK/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 15:22:24,806 - freqtrade.data.history.idatahandler - WARNING - VET/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 15:22:24,955 - freqtrade.data.history.idatahandler - WARNING - BAKE/USDT:USDT, futures, 15m, data starts at 2021-05-19 07:00:00
2023-12-19 15:22:25,102 - freqtrade.data.history.idatahandler - WARNING - UNFI/USDT:USDT, futures, 15m, data starts at 2021-02-19 07:00:00
2023-12-19 15:22:25,277 - freqtrade.data.history.idatahandler - WARNING - RSR/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 15:22:25,450 - freqtrade.data.history.idatahandler - WARNING - LRC/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 15:22:25,601 - freqtrade.data.history.idatahandler - WARNING - CRV/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 15:22:25,752 - freqtrade.data.history.idatahandler - WARNING - C98/USDT:USDT, futures, 15m, data starts at 2021-08-24 03:30:00
2023-12-19 15:22:25,879 - freqtrade.data.history.idatahandler - WARNING - ICP/USDT:USDT, futures, 15m, data starts at 2022-09-27 02:30:00
2023-12-19 15:22:25,983 - freqtrade.data.history.idatahandler - WARNING - LPT/USDT:USDT, futures, 15m, data starts at 2021-11-11 03:30:00
2023-12-19 15:22:26,090 - freqtrade.optimize.backtesting - INFO - Loading data from 2021-01-01 00:00:00 up to 2023-12-12 00:00:00 (1075 days).
2023-12-19 15:22:26,090 - freqtrade.configuration.timerange - WARNING - Moving start-date by 30 candles to account for startup time.
2023-12-19 15:22:26,105 - freqtrade.data.history.idatahandler - WARNING - ATA/USDT:USDT, funding_rate, 8h, data starts at 2021-08-30 08:00:00
2023-12-19 15:22:26,148 - freqtrade.data.history.idatahandler - WARNING - IMX/USDT:USDT, funding_rate, 8h, data starts at 2022-02-11 08:00:00
2023-12-19 15:22:26,182 - freqtrade.data.history.idatahandler - WARNING - OP/USDT:USDT, funding_rate, 8h, data starts at 2022-06-01 08:00:00
2023-12-19 15:22:26,222 - freqtrade.data.history.idatahandler - WARNING - IOTX/USDT:USDT, funding_rate, 8h, data starts at 2021-08-11 16:00:00
2023-12-19 15:22:26,261 - freqtrade.data.history.idatahandler - WARNING - WOO/USDT:USDT, funding_rate, 8h, data starts at 2022-04-07 16:00:00
2023-12-19 15:22:26,374 - freqtrade.data.history.idatahandler - WARNING - BAKE/USDT:USDT, funding_rate, 8h, data starts at 2021-05-19 08:00:00
2023-12-19 15:22:26,570 - freqtrade.data.history.idatahandler - WARNING - C98/USDT:USDT, funding_rate, 8h, data starts at 2021-08-24 08:00:00
2023-12-19 15:22:26,614 - freqtrade.data.history.idatahandler - WARNING - ICP/USDT:USDT, funding_rate, 8h, data starts at 2021-05-11 08:00:00
2023-12-19 15:22:26,660 - freqtrade.data.history.idatahandler - WARNING - LPT/USDT:USDT, funding_rate, 8h, data starts at 2021-11-11 08:00:00
2023-12-19 15:22:26,700 - freqtrade.data.history.idatahandler - WARNING - ATA/USDT:USDT, mark, 8h, data starts at 2021-08-30 00:00:00
2023-12-19 15:22:26,743 - freqtrade.data.history.idatahandler - WARNING - IMX/USDT:USDT, mark, 8h, data starts at 2022-02-11 00:00:00
2023-12-19 15:22:26,786 - freqtrade.data.history.idatahandler - WARNING - OP/USDT:USDT, mark, 8h, data starts at 2022-06-01 00:00:00
2023-12-19 15:22:26,833 - freqtrade.data.history.idatahandler - WARNING - IOTX/USDT:USDT, mark, 8h, data starts at 2021-08-11 08:00:00
2023-12-19 15:22:26,870 - freqtrade.data.history.idatahandler - WARNING - WOO/USDT:USDT, mark, 8h, data starts at 2022-04-07 08:00:00
2023-12-19 15:22:26,991 - freqtrade.data.history.idatahandler - WARNING - BAKE/USDT:USDT, mark, 8h, data starts at 2021-05-19 00:00:00
2023-12-19 15:22:27,211 - freqtrade.data.history.idatahandler - WARNING - C98/USDT:USDT, mark, 8h, data starts at 2021-08-24 00:00:00
2023-12-19 15:22:27,251 - freqtrade.data.history.idatahandler - WARNING - ICP/USDT:USDT, mark, 8h, data starts at 2021-05-11 00:00:00
2023-12-19 15:22:27,289 - freqtrade.data.history.idatahandler - WARNING - LPT/USDT:USDT, mark, 8h, data starts at 2021-11-11 00:00:00
2023-12-19 15:22:27,372 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2023-12-19 15:22:27,385 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy RSI_BB_MACD_Dec_2023_15m_3_rls
2023-12-19 15:22:27,385 - freqtrade.strategy.hyper - INFO - No params for buy found, using default values.
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_max_1 = 6.5
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_max_2 = 50.7
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_min_1 = 5.7
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_min_2 = 20.9
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_max_1 = 21.4
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_max_2 = 50.8
2023-12-19 15:22:27,386 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_min_1 = 9.9
2023-12-19 15:22:27,387 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_min_2 = 30.3
2023-12-19 15:22:27,387 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): bb_tp_l = 16
2023-12-19 15:22:27,387 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): bb_tp_s = 20
2023-12-19 15:22:27,387 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): df24h_val = 20
2023-12-19 15:22:27,387 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): df36h_val = 29
2023-12-19 15:22:27,387 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): leverage_num = 5
2023-12-19 15:22:27,388 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): rsi_tp_l = 22
2023-12-19 15:22:27,388 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): rsi_tp_s = 17
2023-12-19 15:22:27,388 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check = 38
2023-12-19 15:22:27,388 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_s = 20
2023-12-19 15:22:27,388 - freqtrade.strategy.hyper - INFO - No params for sell found, using default values.
2023-12-19 15:22:27,389 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): atr_long_mul = 3.8
2023-12-19 15:22:27,389 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): atr_short_mul = 5.0
2023-12-19 15:22:27,389 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): ema_period_l_exit = 91
2023-12-19 15:22:27,389 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): ema_period_s_exit = 147
2023-12-19 15:22:27,390 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_exit = 19
2023-12-19 15:22:27,390 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_exit_s = 41
2023-12-19 15:22:27,390 - freqtrade.strategy.hyper - INFO - No params for protection found, using default values.
2023-12-19 15:22:27,390 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_allowed_drawdown = 0.1
2023-12-19 15:22:27,391 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_lookback = 2
2023-12-19 15:22:27,391 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_stop_duration = 4
2023-12-19 15:22:27,391 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_trade_limit = 1
2023-12-19 15:22:27,391 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_lookback = 8
2023-12-19 15:22:27,391 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_stop_duration = 4
2023-12-19 15:22:27,391 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_trade_limit = 1
2023-12-19 15:22:29,592 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2021-01-01 07:30:00 up to 2023-12-12 00:00:00 (1074 days).
2023-12-19 15:22:29,608 - freqtrade.resolvers.iresolver - INFO - Using resolved protection MaxDrawdown from '/freqtrade/freqtrade/plugins/protections/max_drawdown_protection.py'...
2023-12-19 15:22:29,621 - freqtrade.resolvers.iresolver - INFO - Using resolved protection StoplossGuard from '/freqtrade/freqtrade/plugins/protections/stoploss_guard.py'...
2023-12-19 18:59:24,109 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-12-19_18-59-24.meta.json"
2023-12-19 18:59:24,110 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-12-19_18-59-24.json"
2023-12-19 18:59:25,866 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy RSI_BB_MACD_Dec_2023_15m_3_rls
============================================================== BACKTESTING REPORT ==============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| UNFI/USDT:USDT |      2685 |           1.30 |        3488.24 |           692.551 |          69.26 |        2:13:00 |  2254     0   431  83.9 |
|  LRC/USDT:USDT |      2367 |           1.12 |        2662.09 |           530.345 |          53.03 |        2:28:00 |  1991     0   376  84.1 |
|  CTK/USDT:USDT |      3395 |           0.77 |        2614.53 |           517.846 |          51.78 |        3:11:00 |  2851     0   544  84.0 |
|  RSR/USDT:USDT |      2717 |           0.91 |        2482.43 |           496.307 |          49.63 |        1:59:00 |  2254     0   463  83.0 |
| BAKE/USDT:USDT |      2359 |           1.02 |        2400.01 |           477.453 |          47.75 |        2:45:00 |  1985     0   374  84.1 |
|  VET/USDT:USDT |      3182 |           0.73 |        2318.45 |           463.398 |          46.34 |        3:10:00 |  2657     0   525  83.5 |
|  IMX/USDT:USDT |      2412 |           0.94 |        2257.87 |           449.469 |          44.95 |        2:55:00 |  2040     0   372  84.6 |
|  CRV/USDT:USDT |      2375 |           0.95 |        2245.05 |           448.396 |          44.84 |        2:06:00 |  1964     0   411  82.7 |
|  ATA/USDT:USDT |      2592 |           0.86 |        2224.17 |           443.924 |          44.39 |        3:41:00 |  2192     0   400  84.6 |
|   OP/USDT:USDT |      1740 |           1.10 |        1921.92 |           384.047 |          38.40 |        2:43:00 |  1462     0   278  84.0 |
| IOTX/USDT:USDT |      2462 |           0.70 |        1735.42 |           346.904 |          34.69 |        3:34:00 |  2063     0   399  83.8 |
|  C98/USDT:USDT |       970 |           1.46 |        1415.63 |           280.731 |          28.07 |        2:50:00 |   824     0   146  84.9 |
|  WOO/USDT:USDT |      1658 |           0.71 |        1172.48 |           234.136 |          23.41 |        3:02:00 |  1404     0   254  84.7 |
|  LPT/USDT:USDT |       757 |           1.41 |        1069.69 |           211.409 |          21.14 |        3:12:00 |   655     0   102  86.5 |
|  ICP/USDT:USDT |       306 |           1.43 |         438.52 |            85.663 |           8.57 |        4:11:00 |   265     0    41  86.6 |
|          TOTAL |     31977 |           0.95 |       30446.50 |          6062.577 |         606.26 |        2:51:00 | 26861     0  5116  84.0 |
=========================================================== LEFT OPEN TRADES REPORT ============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| IOTX/USDT:USDT |         1 |           0.18 |           0.18 |             0.036 |           0.00 |        1:00:00 |     1     0     0   100 |
|   OP/USDT:USDT |         1 |          -2.27 |          -2.27 |            -0.454 |          -0.05 |        0:30:00 |     0     0     1     0 |
|  IMX/USDT:USDT |         1 |         -20.53 |         -20.53 |            -4.065 |          -0.41 |        2:15:00 |     0     0     1     0 |
|  CTK/USDT:USDT |         1 |         -26.00 |         -26.00 |            -5.178 |          -0.52 |        5:15:00 |     0     0     1     0 |
|          TOTAL |         4 |         -12.16 |         -48.63 |            -9.662 |          -0.97 |        2:15:00 |     1     0     3  25.0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     31977 |           0.95 |       30446.50 |          6062.577 |         606.26 |        2:51:00 | 26861     0  5116  84.0 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   27287 |  25706     0  1581  94.2 |           3.99 |      108904    |         21701.7   |       21780.9  |
|          stop_loss |    2269 |      0     0  2269     0 |         -31.8  |      -72156.5  |        -14377.7   |      -14431.3  |
|                roi |    1180 |   1154     0    26  97.8 |          14.12 |       16658.8  |          3318.38  |        3331.75 |
|         exit_short |    1091 |      0     0  1091     0 |         -18.35 |      -20017.3  |         -3992.99  |       -4003.47 |
|          exit_long |     146 |      0     0   146     0 |         -19.82 |       -2894.12 |          -577.21  |        -578.82 |
|         force_exit |       4 |      1     0     3  25.0 |         -12.16 |         -48.63 |            -9.662 |          -9.73 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |           295.071 |    917 |       0 |      237 |
| 28/02/2021 |           300.852 |    850 |       0 |      198 |
| 31/03/2021 |            83.645 |    885 |       0 |      177 |
| 30/04/2021 |           207.629 |    849 |       0 |      205 |
| 31/05/2021 |           436.161 |   1085 |       0 |      250 |
| 30/06/2021 |           223.445 |   1015 |       0 |      183 |
| 31/07/2021 |            77.659 |    790 |       0 |      148 |
| 31/08/2021 |           306.828 |   1068 |       0 |      184 |
| 30/09/2021 |           250.467 |    854 |       0 |      148 |
| 31/10/2021 |             0.447 |    762 |       0 |      161 |
| 30/11/2021 |           183.28  |    910 |       0 |      182 |
| 31/12/2021 |           291.636 |    888 |       0 |      154 |
| 31/01/2022 |            82.941 |    753 |       0 |      145 |
| 28/02/2022 |           -12.872 |    668 |       0 |      149 |
| 31/03/2022 |            -4.367 |    711 |       0 |      159 |
| 30/04/2022 |           228.965 |    688 |       0 |      127 |
| 31/05/2022 |           469.186 |   1315 |       0 |      257 |
| 30/06/2022 |           487.807 |   1235 |       0 |      261 |
| 31/07/2022 |           164.131 |    970 |       0 |      193 |
| 31/08/2022 |            64.17  |    690 |       0 |      118 |
| 30/09/2022 |           127.387 |    511 |       0 |       78 |
| 31/10/2022 |           120.245 |    486 |       0 |       80 |
| 30/11/2022 |           145.669 |    745 |       0 |      140 |
| 31/12/2022 |           131.705 |    385 |       0 |       48 |
| 31/01/2023 |           134.219 |    716 |       0 |      133 |
| 28/02/2023 |           230.782 |    847 |       0 |      134 |
| 31/03/2023 |           265.093 |    843 |       0 |      121 |
| 30/04/2023 |            41.971 |    523 |       0 |       98 |
| 31/05/2023 |            64.934 |    457 |       0 |       69 |
| 30/06/2023 |            88.62  |    521 |       0 |       83 |
| 31/07/2023 |            83.865 |    394 |       0 |       62 |
| 31/08/2023 |            48.722 |    490 |       0 |      102 |
| 30/09/2023 |            75.459 |    426 |       0 |       65 |
| 31/10/2023 |            91.669 |    524 |       0 |       99 |
| 30/11/2023 |           214.637 |    792 |       0 |      118 |
| 31/12/2023 |            60.52  |    298 |       0 |       50 |
==================== SUMMARY METRICS ====================
| Metric                      | Value                   |
|-----------------------------+-------------------------|
| Backtesting from            | 2021-01-01 07:30:00     |
| Backtesting to              | 2023-12-12 00:00:00     |
| Max open trades             | 5                       |
|                             |                         |
| Total/Daily Avg Trades      | 31977 / 29.77           |
| Starting balance            | 1000 USDT               |
| Final balance               | 7062.577 USDT           |
| Absolute profit             | 6062.577 USDT           |
| Total profit %              | 606.26%                 |
| CAGR %                      | 94.32%                  |
| Sortino                     | 42.36                   |
| Sharpe                      | 49.56                   |
| Calmar                      | 252.55                  |
| Profit factor               | 1.30                    |
| Expectancy (Ratio)          | 0.19 (0.05)             |
| Trades per day              | 29.77                   |
| Avg. daily profit %         | 0.56%                   |
| Avg. stake amount           | 19.932 USDT             |
| Total trade volume          | 637370.545 USDT         |
|                             |                         |
| Long / Short                | 3176 / 28801            |
| Total profit Long %         | 59.63%                  |
| Total profit Short %        | 546.62%                 |
| Absolute profit Long        | 596.335 USDT            |
| Absolute profit Short       | 5466.242 USDT           |
|                             |                         |
| Best Pair                   | UNFI/USDT:USDT 3488.24% |
| Worst Pair                  | ICP/USDT:USDT 438.52%   |
| Best trade                  | CTK/USDT:USDT 19.63%    |
| Worst trade                 | VET/USDT:USDT -35.50%   |
| Best day                    | 79.29 USDT              |
| Worst day                   | -59.331 USDT            |
| Days win/draw/lose          | 632 / 1 / 443           |
| Avg. Duration Winners       | 2:12:00                 |
| Avg. Duration Loser         | 6:16:00                 |
| Max Consecutive Wins / Loss | 73 / 9                  |
| Rejected Entry signals      | 195602                  |
| Entry/Exit Timeouts         | 0 / 10165               |
|                             |                         |
| Min balance                 | 969.489 USDT            |
| Max balance                 | 7072.239 USDT           |
| Max % of account underwater | 5.77%                   |
| Absolute Drawdown (Account) | 4.27%                   |
| Absolute Drawdown           | 164.673 USDT            |
| Drawdown high               | 2856.318 USDT           |
| Drawdown low                | 2691.645 USDT           |
| Drawdown Start              | 2022-03-15 09:45:00     |
| Drawdown End                | 2022-03-28 10:30:00     |
| Market change               | -36.56%                 |
=========================================================

Backtested 2021-01-01 07:30:00 -> 2023-12-12 00:00:00 | Max open trades : 5
================================================================================ STRATEGY SUMMARY ===============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |            Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+---------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     31977 |           0.95 |       30446.50 |          6062.577 |         606.26 |        2:51:00 | 26861     0  5116  84.0 | 164.673 USDT  4.27% |
=================================================================================================================================================================================






sudo docker compose run freqtrade backtesting --strategy RSI_BB_MACD_Dec_2023_15m_3_rls -i 15m --export trades --breakdown month --timerange 20210101-20231212 --enable-protections
[sudo] password for picasso999:
2023-12-19 19:08:54,159 - freqtrade - INFO - freqtrade 2023.10
2023-12-19 19:08:54,185 - freqtrade.configuration.load_config - INFO - Using config: user_data/config.json ...
2023-12-19 19:08:54,186 - freqtrade.loggers - INFO - Verbosity set to 0
2023-12-19 19:08:54,187 - freqtrade.configuration.configuration - INFO - Parameter -i/--timeframe detected ... Using timeframe: 15m ...
2023-12-19 19:08:54,187 - freqtrade.configuration.configuration - INFO - Parameter --enable-protections detected, enabling Protections. ...
2023-12-19 19:08:54,187 - freqtrade.configuration.configuration - INFO - Using max_open_trades: -1 ...
2023-12-19 19:08:54,187 - freqtrade.configuration.configuration - INFO - Parameter --timerange detected: 20210101-20231212 ...
2023-12-19 19:08:54,267 - freqtrade.configuration.configuration - INFO - Using user-data directory: /freqtrade/user_data ...
2023-12-19 19:08:54,268 - freqtrade.configuration.configuration - INFO - Using data directory: /freqtrade/user_data/data/binance ...
2023-12-19 19:08:54,268 - freqtrade.configuration.configuration - INFO - Overriding timeframe with Command line argument
2023-12-19 19:08:54,268 - freqtrade.configuration.configuration - INFO - Parameter --export detected: trades ...
2023-12-19 19:08:54,268 - freqtrade.configuration.configuration - INFO - Parameter --breakdown detected ...
2023-12-19 19:08:54,268 - freqtrade.configuration.configuration - INFO - Parameter --cache=day detected ...
2023-12-19 19:08:54,268 - freqtrade.configuration.configuration - INFO - Filter trades by timerange: 20210101-20231212
2023-12-19 19:08:54,269 - freqtrade.exchange.check_exchange - INFO - Checking exchange...
2023-12-19 19:08:54,287 - freqtrade.exchange.check_exchange - INFO - Exchange "binance" is officially supported by the Freqtrade development team.
2023-12-19 19:08:54,287 - freqtrade.configuration.configuration - INFO - Using pairlist from configuration.
2023-12-19 19:08:54,287 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2023-12-19 19:08:54,295 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2023-12-19 19:08:54,296 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2023-12-19 19:08:54,296 - freqtrade.exchange.exchange - INFO - Using CCXT 4.1.22
2023-12-19 19:08:54,296 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}, 'enableRateLimit': True}
2023-12-19 19:08:54,316 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}, 'enableRateLimit': True, 'rateLimit': 50}
2023-12-19 19:08:54,339 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2023-12-19 19:09:00,792 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2023-12-19 19:09:02,079 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy RSI_BB_MACD_Dec_2023_15m_3_rls from '/freqtrade/user_data/strategies/RSI_BB_MACD_Dec_2023_15m_3_rls.py'...
2023-12-19 19:09:02,079 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2023-12-19 19:09:02,080 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 15m.
2023-12-19 19:09:02,080 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2023-12-19 19:09:02,080 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 20.
2023-12-19 19:09:02,080 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'entry': 10, 'exit': 10, 'exit_timeout_count': 0, 'unit': 'minutes'}.
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'max_open_trades' with value in config file: inf.
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.184, '416': 0.14, '933': 0.073, '1982': 0}
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 15m
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.317
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: True
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive: 0.012
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.03
2023-12-19 19:09:02,081 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: True
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: False
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: True
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'entry': 'GTC', 'exit': 'GTC'}
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 20
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using protections: [{'method': 'MaxDrawdown', 'lookback_period_candles': 2, 'trade_limit': 1, 'stop_duration_candles': 4, 'max_allowed_drawdown': 0.1}, {'method': 'StoplossGuard', 'lookback_period_candles': 8, 'trade_limit': 1, 'stop_duration_candles': 4, 'only_per_pair': False}]
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using startup_candle_count: 30
2023-12-19 19:09:02,082 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using unfilledtimeout: {'entry': 10, 'exit': 10, 'exit_timeout_count': 0, 'unit': 'minutes'}
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_exit_signal: True
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_only: False
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2023-12-19 19:09:02,083 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2023-12-19 19:09:02,084 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: inf
2023-12-19 19:09:02,084 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2023-12-19 19:09:02,133 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist StaticPairList from '/freqtrade/freqtrade/plugins/pairlist/StaticPairList.py'...
2023-12-19 19:09:02,193 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist AgeFilter from '/freqtrade/freqtrade/plugins/pairlist/AgeFilter.py'...
2023-12-19 19:09:02,214 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist VolatilityFilter from '/freqtrade/freqtrade/plugins/pairlist/VolatilityFilter.py'...
2023-12-19 19:09:02,225 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist RangeStabilityFilter from '/freqtrade/freqtrade/plugins/pairlist/rangestabilityfilter.py'...
2023-12-19 19:09:02,251 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist ShuffleFilter from '/freqtrade/freqtrade/plugins/pairlist/ShuffleFilter.py'...
2023-12-19 19:09:02,251 - ShuffleFilter - INFO - Backtesting mode detected, applying seed value: None
2023-12-19 19:10:18,812 - freqtrade.data.history.history_utils - INFO - Using indicator startup period: 30 ...
2023-12-19 19:10:18,893 - freqtrade.data.history.idatahandler - WARNING - C98/USDT:USDT, futures, 15m, data starts at 2021-08-24 03:30:00
2023-12-19 19:10:19,039 - freqtrade.data.history.idatahandler - WARNING - WOO/USDT:USDT, futures, 15m, data starts at 2022-04-08 03:30:00
2023-12-19 19:10:19,132 - freqtrade.data.history.idatahandler - WARNING - BAKE/USDT:USDT, futures, 15m, data starts at 2021-05-19 07:00:00
2023-12-19 19:10:19,286 - freqtrade.data.history.idatahandler - WARNING - UNFI/USDT:USDT, futures, 15m, data starts at 2021-02-19 07:00:00
2023-12-19 19:10:19,431 - freqtrade.data.history.idatahandler - WARNING - RSR/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 19:10:19,618 - freqtrade.data.history.idatahandler - WARNING - IMX/USDT:USDT, futures, 15m, data starts at 2022-02-11 03:30:00
2023-12-19 19:10:19,763 - freqtrade.data.history.idatahandler - WARNING - VET/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 19:10:19,918 - freqtrade.data.history.idatahandler - WARNING - CTK/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 19:10:20,065 - freqtrade.data.history.idatahandler - WARNING - IOTX/USDT:USDT, futures, 15m, data starts at 2021-08-12 03:30:00
2023-12-19 19:10:20,179 - freqtrade.data.history.idatahandler - WARNING - LRC/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 19:10:20,315 - freqtrade.data.history.idatahandler - WARNING - CRV/USDT:USDT, futures, 15m, data starts at 2021-01-01 00:00:00
2023-12-19 19:10:20,462 - freqtrade.data.history.idatahandler - WARNING - OP/USDT:USDT, futures, 15m, data starts at 2022-06-01 14:00:00
2023-12-19 19:10:20,569 - freqtrade.data.history.idatahandler - WARNING - ICP/USDT:USDT, futures, 15m, data starts at 2022-09-27 02:30:00
2023-12-19 19:10:20,665 - freqtrade.data.history.idatahandler - WARNING - LPT/USDT:USDT, futures, 15m, data starts at 2021-11-11 03:30:00
2023-12-19 19:10:20,801 - freqtrade.data.history.idatahandler - WARNING - ATA/USDT:USDT, futures, 15m, data starts at 2021-08-31 03:30:00
2023-12-19 19:10:20,906 - freqtrade.optimize.backtesting - INFO - Loading data from 2021-01-01 00:00:00 up to 2023-12-12 00:00:00 (1075 days).
2023-12-19 19:10:20,907 - freqtrade.configuration.timerange - WARNING - Moving start-date by 30 candles to account for startup time.
2023-12-19 19:10:20,921 - freqtrade.data.history.idatahandler - WARNING - C98/USDT:USDT, funding_rate, 8h, data starts at 2021-08-24 08:00:00
2023-12-19 19:10:20,954 - freqtrade.data.history.idatahandler - WARNING - WOO/USDT:USDT, funding_rate, 8h, data starts at 2022-04-07 16:00:00
2023-12-19 19:10:20,991 - freqtrade.data.history.idatahandler - WARNING - BAKE/USDT:USDT, funding_rate, 8h, data starts at 2021-05-19 08:00:00
2023-12-19 19:10:21,112 - freqtrade.data.history.idatahandler - WARNING - IMX/USDT:USDT, funding_rate, 8h, data starts at 2022-02-11 08:00:00
2023-12-19 19:10:21,227 - freqtrade.data.history.idatahandler - WARNING - IOTX/USDT:USDT, funding_rate, 8h, data starts at 2021-08-11 16:00:00
2023-12-19 19:10:21,342 - freqtrade.data.history.idatahandler - WARNING - OP/USDT:USDT, funding_rate, 8h, data starts at 2022-06-01 08:00:00
2023-12-19 19:10:21,378 - freqtrade.data.history.idatahandler - WARNING - ICP/USDT:USDT, funding_rate, 8h, data starts at 2021-05-11 08:00:00
2023-12-19 19:10:21,412 - freqtrade.data.history.idatahandler - WARNING - LPT/USDT:USDT, funding_rate, 8h, data starts at 2021-11-11 08:00:00
2023-12-19 19:10:21,453 - freqtrade.data.history.idatahandler - WARNING - ATA/USDT:USDT, funding_rate, 8h, data starts at 2021-08-30 08:00:00
2023-12-19 19:10:21,493 - freqtrade.data.history.idatahandler - WARNING - C98/USDT:USDT, mark, 8h, data starts at 2021-08-24 00:00:00
2023-12-19 19:10:21,529 - freqtrade.data.history.idatahandler - WARNING - WOO/USDT:USDT, mark, 8h, data starts at 2022-04-07 08:00:00
2023-12-19 19:10:21,571 - freqtrade.data.history.idatahandler - WARNING - BAKE/USDT:USDT, mark, 8h, data starts at 2021-05-19 00:00:00
2023-12-19 19:10:21,700 - freqtrade.data.history.idatahandler - WARNING - IMX/USDT:USDT, mark, 8h, data starts at 2022-02-11 00:00:00
2023-12-19 19:10:21,810 - freqtrade.data.history.idatahandler - WARNING - IOTX/USDT:USDT, mark, 8h, data starts at 2021-08-11 08:00:00
2023-12-19 19:10:21,937 - freqtrade.data.history.idatahandler - WARNING - OP/USDT:USDT, mark, 8h, data starts at 2022-06-01 00:00:00
2023-12-19 19:10:21,987 - freqtrade.data.history.idatahandler - WARNING - ICP/USDT:USDT, mark, 8h, data starts at 2021-05-11 00:00:00
2023-12-19 19:10:22,028 - freqtrade.data.history.idatahandler - WARNING - LPT/USDT:USDT, mark, 8h, data starts at 2021-11-11 00:00:00
2023-12-19 19:10:22,074 - freqtrade.data.history.idatahandler - WARNING - ATA/USDT:USDT, mark, 8h, data starts at 2021-08-30 00:00:00
2023-12-19 19:10:22,167 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2023-12-19 19:10:22,176 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy RSI_BB_MACD_Dec_2023_15m_3_rls
2023-12-19 19:10:22,176 - freqtrade.strategy.hyper - INFO - No params for buy found, using default values.
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_max_1 = 6.5
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_max_2 = 50.7
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_min_1 = 5.7
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_long_min_2 = 20.9
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_max_1 = 21.4
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_max_2 = 50.8
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_min_1 = 9.9
2023-12-19 19:10:22,177 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): adx_short_min_2 = 30.3
2023-12-19 19:10:22,178 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): bb_tp_l = 16
2023-12-19 19:10:22,178 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): bb_tp_s = 20
2023-12-19 19:10:22,178 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): df24h_val = 20
2023-12-19 19:10:22,178 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): df36h_val = 29
2023-12-19 19:10:22,178 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): leverage_num = 5
2023-12-19 19:10:22,179 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): rsi_tp_l = 22
2023-12-19 19:10:22,179 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): rsi_tp_s = 17
2023-12-19 19:10:22,179 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check = 38
2023-12-19 19:10:22,179 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_s = 20
2023-12-19 19:10:22,179 - freqtrade.strategy.hyper - INFO - No params for sell found, using default values.
2023-12-19 19:10:22,180 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): atr_long_mul = 3.8
2023-12-19 19:10:22,180 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): atr_short_mul = 5.0
2023-12-19 19:10:22,180 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): ema_period_l_exit = 91
2023-12-19 19:10:22,180 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): ema_period_s_exit = 147
2023-12-19 19:10:22,181 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_exit = 19
2023-12-19 19:10:22,181 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): volume_check_exit_s = 41
2023-12-19 19:10:22,181 - freqtrade.strategy.hyper - INFO - No params for protection found, using default values.
2023-12-19 19:10:22,181 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_allowed_drawdown = 0.1
2023-12-19 19:10:22,182 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_lookback = 2
2023-12-19 19:10:22,182 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_stop_duration = 4
2023-12-19 19:10:22,182 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): max_drawdown_trade_limit = 1
2023-12-19 19:10:22,182 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_lookback = 8
2023-12-19 19:10:22,182 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_stop_duration = 4
2023-12-19 19:10:22,182 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): stoploss_guard_trade_limit = 1
2023-12-19 19:10:24,514 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2021-01-01 07:30:00 up to 2023-12-12 00:00:00 (1074 days).
2023-12-19 19:10:24,530 - freqtrade.resolvers.iresolver - INFO - Using resolved protection MaxDrawdown from '/freqtrade/freqtrade/plugins/protections/max_drawdown_protection.py'...
2023-12-19 19:10:24,542 - freqtrade.resolvers.iresolver - INFO - Using resolved protection StoplossGuard from '/freqtrade/freqtrade/plugins/protections/stoploss_guard.py'...
2023-12-19 21:27:10,830 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-12-19_21-27-10.meta.json"
2023-12-19 21:27:10,831 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-12-19_21-27-10.json"
2023-12-19 21:27:14,513 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy RSI_BB_MACD_Dec_2023_15m_3_rls
============================================================== BACKTESTING REPORT ==============================================================
|           Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|----------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|  LRC/USDT:USDT |      4302 |           1.06 |        4553.35 |           906.580 |          90.66 |        3:08:00 |  3661     0   641  85.1 |
|  CRV/USDT:USDT |      4781 |           0.91 |        4366.70 |           872.265 |          87.23 |        2:37:00 |  4033     0   748  84.4 |
| UNFI/USDT:USDT |      4457 |           0.91 |        4057.11 |           805.321 |          80.53 |        2:41:00 |  3730     0   727  83.7 |
| BAKE/USDT:USDT |      3778 |           1.04 |        3940.22 |           784.418 |          78.44 |        3:08:00 |  3214     0   564  85.1 |
|  RSR/USDT:USDT |      4807 |           0.80 |        3825.19 |           764.791 |          76.48 |        2:37:00 |  4036     0   771  84.0 |
|  C98/USDT:USDT |      3294 |           1.16 |        3826.45 |           758.783 |          75.88 |        3:18:00 |  2824     0   470  85.7 |
| IOTX/USDT:USDT |      3098 |           0.89 |        2769.62 |           553.651 |          55.37 |        3:35:00 |  2635     0   463  85.1 |
|  VET/USDT:USDT |      4063 |           0.67 |        2714.17 |           542.518 |          54.25 |        3:29:00 |  3408     0   655  83.9 |
|  IMX/USDT:USDT |      2787 |           0.87 |        2415.09 |           480.530 |          48.05 |        3:03:00 |  2356     0   431  84.5 |
|  CTK/USDT:USDT |      3931 |           0.61 |        2388.51 |           473.400 |          47.34 |        3:35:00 |  3301     0   630  84.0 |
|   OP/USDT:USDT |      2240 |           1.01 |        2258.82 |           451.286 |          45.13 |        2:57:00 |  1877     0   363  83.8 |
|  LPT/USDT:USDT |      2670 |           0.84 |        2231.93 |           443.193 |          44.32 |        3:42:00 |  2289     2   379  85.7 |
|  ATA/USDT:USDT |      2874 |           0.58 |        1668.76 |           332.731 |          33.27 |        3:43:00 |  2429     0   445  84.5 |
|  WOO/USDT:USDT |      2405 |           0.65 |        1569.33 |           313.386 |          31.34 |        3:20:00 |  2055     0   350  85.4 |
|  ICP/USDT:USDT |      1195 |           0.71 |         853.48 |           166.604 |          16.66 |        5:22:00 |  1016     0   179  85.0 |
|          TOTAL |     50682 |           0.86 |       43438.72 |          8649.456 |         864.95 |        3:13:00 | 42864     2  7816  84.6 |
=========================================================== LEFT OPEN TRADES REPORT ===========================================================
|          Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|---------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| CTK/USDT:USDT |         1 |         -26.00 |         -26.00 |            -5.178 |          -0.52 |        5:15:00 |     0     0     1     0 |
|         TOTAL |         1 |         -26.00 |         -26.00 |            -5.178 |          -0.52 |        5:15:00 |     0     0     1     0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     50682 |           0.86 |       43438.72 |          8649.456 |         864.95 |        3:13:00 | 42864     2  7816  84.6 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   43344 |  41258     0  2086  95.2 |           3.91 |      169399    |         33752.8   |       11293.3  |
|          stop_loss |    3273 |      0     0  3273     0 |         -31.82 |     -104135    |        -20748.5   |       -6942.33 |
|         exit_short |    1928 |      1     0  1927   0.1 |         -18.38 |      -35430    |         -7062.67  |       -2362    |
|                roi |    1678 |   1605     2    71  95.6 |          12.9  |       21651.8  |          4313.52  |        1443.46 |
|          exit_long |     458 |      0     0   458     0 |         -17.51 |       -8021.45 |         -1600.53  |        -534.76 |
|         force_exit |       1 |      0     0     1     0 |         -26    |         -26    |            -5.178 |          -1.73 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |           297.676 |    907 |       0 |      236 |
| 28/02/2021 |           297.259 |    851 |       0 |      201 |
| 31/03/2021 |            85.331 |    896 |       0 |      185 |
| 30/04/2021 |           238.611 |    894 |       0 |      210 |
| 31/05/2021 |           424.459 |   1125 |       0 |      266 |
| 30/06/2021 |           318.439 |   1159 |       0 |      195 |
| 31/07/2021 |            87.669 |    921 |       0 |      183 |
| 31/08/2021 |           340.392 |   1219 |       0 |      201 |
| 30/09/2021 |           316.329 |   1254 |       0 |      217 |
| 31/10/2021 |           121.468 |   1119 |       0 |      203 |
| 30/11/2021 |           219.379 |   1349 |       0 |      255 |
| 31/12/2021 |           460.935 |   1385 |       0 |      220 |
| 31/01/2022 |            77.652 |   1107 |       0 |      205 |
| 28/02/2022 |           -13.102 |   1023 |       0 |      225 |
| 31/03/2022 |           182.769 |   1361 |       0 |      260 |
| 30/04/2022 |           415.909 |   1192 |       0 |      176 |
| 31/05/2022 |           725.915 |   2155 |       0 |      396 |
| 30/06/2022 |           696.01  |   2036 |       0 |      419 |
| 31/07/2022 |           170.591 |   1511 |       0 |      298 |
| 31/08/2022 |           261.049 |   1389 |       0 |      215 |
| 30/09/2022 |           272.274 |   1187 |       0 |      172 |
| 31/10/2022 |           222.167 |   1046 |       0 |      179 |
| 30/11/2022 |           300.927 |   1340 |       0 |      247 |
| 31/12/2022 |           231.854 |    864 |       0 |      129 |
| 31/01/2023 |           133.313 |   1349 |       0 |      249 |
| 28/02/2023 |           397.793 |   1486 |       0 |      218 |
| 31/03/2023 |           314.028 |   1585 |       0 |      229 |
| 30/04/2023 |           171.297 |   1177 |       0 |      190 |
| 31/05/2023 |           145.722 |    957 |       0 |      152 |
| 30/06/2023 |            89.135 |    968 |       0 |      172 |
| 31/07/2023 |           183.999 |   1003 |       0 |      150 |
| 31/08/2023 |            95.361 |   1046 |       0 |      209 |
| 30/09/2023 |            61.242 |    902 |       2 |      169 |
| 31/10/2023 |           -61.622 |    995 |       0 |      242 |
| 30/11/2023 |           198.467 |   1546 |       0 |      246 |
| 31/12/2023 |           168.758 |    560 |       0 |       97 |
=================== SUMMARY METRICS ====================
| Metric                      | Value                  |
|-----------------------------+------------------------|
| Backtesting from            | 2021-01-01 07:30:00    |
| Backtesting to              | 2023-12-12 00:00:00    |
| Max open trades             | 15                     |
|                             |                        |
| Total/Daily Avg Trades      | 50682 / 47.19          |
| Starting balance            | 1000 USDT              |
| Final balance               | 9649.456 USDT          |
| Absolute profit             | 8649.456 USDT          |
| Total profit %              | 864.95%                |
| CAGR %                      | 116.06%                |
| Sortino                     | 62.06                  |
| Sharpe                      | 73.05                  |
| Calmar                      | 328.71                 |
| Profit factor               | 1.28                   |
| Expectancy (Ratio)          | 0.17 (0.04)            |
| Trades per day              | 47.19                  |
| Avg. daily profit %         | 0.81%                  |
| Avg. stake amount           | 19.929 USDT            |
| Total trade volume          | 1010066.732 USDT       |
|                             |                        |
| Long / Short                | 6493 / 44189           |
| Total profit Long %         | 66.08%                 |
| Total profit Short %        | 798.87%                |
| Absolute profit Long        | 660.784 USDT           |
| Absolute profit Short       | 7988.672 USDT          |
|                             |                        |
| Best Pair                   | LRC/USDT:USDT 4553.35% |
| Worst Pair                  | ICP/USDT:USDT 853.48%  |
| Best trade                  | CTK/USDT:USDT 19.63%   |
| Worst trade                 | UNFI/USDT:USDT -39.46% |
| Best day                    | 102.325 USDT           |
| Worst day                   | -130.604 USDT          |
| Days win/draw/lose          | 662 / 0 / 414          |
| Avg. Duration Winners       | 2:26:00                |
| Avg. Duration Loser         | 7:29:00                |
| Max Consecutive Wins / Loss | 85 / 16                |
| Rejected Entry signals      | 0                      |
| Entry/Exit Timeouts         | 0 / 14483              |
|                             |                        |
| Min balance                 | 968.657 USDT           |
| Max balance                 | 9660.933 USDT          |
| Max % of account underwater | 5.77%                  |
| Absolute Drawdown (Account) | 4.68%                  |
| Absolute Drawdown           | 205.37 USDT            |
| Drawdown high               | 3387.515 USDT          |
| Drawdown low                | 3182.145 USDT          |
| Drawdown Start              | 2022-01-25 09:45:00    |
| Drawdown End                | 2022-02-08 06:30:00    |
| Market change               | -36.56%                |
========================================================

Backtested 2021-01-01 07:30:00 -> 2023-12-12 00:00:00 | Max open trades : 15
=============================================================================== STRATEGY SUMMARY ===============================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |           Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+--------------------|
| RSI_BB_MACD_Dec_2023_15m_3_rls |     50682 |           0.86 |       43438.72 |          8649.456 |         864.95 |        3:13:00 | 42864     2  7816  84.6 | 205.37 USDT  4.68% |
================================================================================================================================================================================

    '''

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
    trailing_stop_positive = 0.012
    trailing_stop_positive_offset = 0.03
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

    df24h_val =  IntParameter(1, 245, default=20, space="buy", optimize= parameters_yes)
    df36h_val =  IntParameter(1, 245, default=29, space="buy", optimize= parameters_yes)

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

    def pump_dump_protection(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        df36h = dataframe.copy().shift(self.df36h_val.value) # 432 mins , 86 for 5m, 29 for 15m
        df24h = dataframe.copy().shift(self.df24h_val.value) # 288 mins, 58 for 5m , 20 for 15m
        dataframe['volume_mean_short'] = dataframe['volume'].rolling(1).mean() # 4 rolling candles
        dataframe['volume_mean_long'] = df24h['volume'].rolling(5).mean() # 48 rolling candles, 10 for 5m
        dataframe['volume_mean_base'] = df36h['volume'].rolling(48).mean() # 238 rolling candles, 48 for 15m
        # dataframe['volume_change_percentage'] = (dataframe['volume_mean_long'] / dataframe['volume_mean_base'])
        # dataframe['rsi_mean'] = dataframe['rsi'].rolling(48).mean() # 48 candles rolling
        dataframe['pnd_volume_warn'] = np.where((dataframe['volume_mean_short'] / dataframe['volume_mean_long'] > 5.0),
                                                -1, 0)
        return dataframe



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

        dataframe = self.pump_dump_protection(dataframe, metadata)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # dataframe.loc[
        #     (
        #                 (
        #                     (dataframe['adx'] > self.adx_long_min_1.value) & # trend strength confirmation
        #                     (dataframe['adx'] < self.adx_long_max_1.value)
        #                 ) |
        #                 (
        #                     (dataframe['adx'] > self.adx_long_min_2.value) & # trend strength confirmation
        #                     (dataframe['adx'] < self.adx_long_max_2.value)
        #                 ) & # trend strength confirmation
        #                 (dataframe['trend_l'] == 1) &
        #                 (dataframe['volume'] > dataframe['volume_mean'])
        #                 (dataframe['volume'] > 0)

        #     ),
        #     'enter_long'] = 1

        # dataframe.loc[
        #     (
        #                 (
        #                     (dataframe['adx'] > self.adx_short_min_1.value) & # trend strength confirmation
        #                     (dataframe['adx'] < self.adx_short_max_1.value)
        #                 ) |
        #                 (
        #                     (dataframe['adx'] > self.adx_short_min_2.value) & # trend strength confirmation
        #                     (dataframe['adx'] < self.adx_short_max_2.value)
        #                 ) & # trend strength confirmation
        #                 (dataframe['trend_s'] == -1) &
        #                 (dataframe['volume'] > dataframe['volume_mean_s']) # volume weighted indicator
        #     ),
        #     'enter_short'] = 1


        conditions_long = []
        conditions_short = []
        dataframe.loc[:, 'entry_tag'] = ''

        buy_1 = (
                        (
                            (dataframe['adx'] > self.adx_long_min_1.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_long_max_1.value)
                        ) |
                        (
                            (dataframe['adx'] > self.adx_long_min_2.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_long_max_2.value)
                        ) & # trend strength confirmation
                        (dataframe['trend_l'] == 1) &
                        (dataframe['volume'] > dataframe['volume_mean']) &
                        (dataframe['volume'] > 0)
        )

        buy_2 = (

                        (   (dataframe['adx'] > self.adx_short_min_1.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_short_max_1.value)
                        ) |
                        (
                            (dataframe['adx'] > self.adx_short_min_2.value) & # trend strength confirmation
                            (dataframe['adx'] < self.adx_short_max_2.value)
                        ) & # trend strength confirmation
                        (dataframe['trend_s'] == -1) &
                        (dataframe['volume'] > dataframe['volume_mean_s']) # volume weighted indicator
        )

        # sell_3 = (
        #         (dataframe['adx'] > self.sell_adx.value) &
        #         (dataframe['l_tema_s'] < dataframe['l_dema_s']) &  # Guard: tema is falling
        #         (dataframe['l_dema_s'] < dataframe['l_ema200_s']) &  # Guard: tema is raising
        #         (dataframe['volume'] > 0)
        # )

        # sell_4 = (
        #         (dataframe['adx'] > self.sell_adx.value) &
        #         (dataframe['l_tema_s'] < dataframe['l_dema_s']) &  # Guard: tema is falling
        #         (dataframe['volume'] > 0)
        # )

        # conditions_long.append(sell_3)
        # dataframe.loc[sell_3, 'entry_tag'] += 'buy_3'

        # conditions_short.append(sell_4)
        # dataframe.loc[sell_4, 'entry_tag'] += 'buy_4'

        conditions_long.append(buy_1)
        dataframe.loc[buy_1, 'entry_tag'] += 'buy_1'

        conditions_short.append(buy_2)
        dataframe.loc[buy_2, 'entry_tag'] += 'buy_2'

        if conditions_long:
            dataframe.loc[
                reduce(lambda x, y: x | y, conditions_long),
                'enter_long'] = 1

        if conditions_short:
            dataframe.loc[
                reduce(lambda x, y: x | y, conditions_short),
                'enter_short'] = 1


        dont_buy_conditions = []

        dont_buy_conditions.append((dataframe['pnd_volume_warn'] < 0.0))

        if conditions_long:
            # combined_conditions = [poc_condition & condition for condition in conditions]
            combined_conditions = [condition for condition in conditions_long]
            final_condition = reduce(lambda x, y: x | y, combined_conditions)
            dataframe.loc[final_condition, 'enter_long'] = 1
        elif conditions_short:
            # combined_conditions = [poc_condition & condition for condition in conditions]
            combined_conditions = [condition for condition in conditions_short]
            final_condition = reduce(lambda x, y: x | y, combined_conditions)
            dataframe.loc[final_condition, 'enter_short'] = 1
        if dont_buy_conditions:
            for condition in dont_buy_conditions:
                dataframe.loc[condition, 'enter_long'] = 0
                dataframe.loc[condition, 'enter_short'] = 0


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
