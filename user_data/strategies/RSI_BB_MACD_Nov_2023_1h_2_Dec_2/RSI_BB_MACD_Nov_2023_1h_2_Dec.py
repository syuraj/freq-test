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


    '''
sudo docker compose run freqtrade backtesting --strategy RSI_BB_MACD_Nov_2023_1h_2_Dec-i 1h --export trades --breakdown month --timerange 20210101-20231027
    

    2023-11-25 08:35:16,439 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 1h.
2023-11-25 08:35:16,439 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2023-11-25 08:35:16,439 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 10.
2023-11-25 08:35:16,439 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'entry': 10, 'exit': 10, 'exit_timeout_count': 0, 'unit': 'minutes'}.
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'max_open_trades' with value in config file: inf.
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.184, '416': 0.14, '933': 0.073, '1982': 0}
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 1h
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.317
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: True
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive: 0.01
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.022
2023-11-25 08:35:16,440 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: True
2023-11-25 08:35:16,441 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: False
2023-11-25 08:35:16,441 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: True
2023-11-25 08:35:16,441 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'entry': 'limit', 'exit': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2023-11-25 08:35:16,441 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'entry': 'GTC', 'exit': 'GTC'}
2023-11-25 08:35:16,441 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2023-11-25 08:35:16,441 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 10

    2023-11-25 08:37:29,625 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy RSI_BB_MACD_Nov_2023_1h_2
2023-11-25 08:37:29,626 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_long_max_1 = 6.5
2023-11-25 08:37:29,626 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_long_max_2 = 50.7
2023-11-25 08:37:29,626 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_long_min_1 = 5.7
2023-11-25 08:37:29,626 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_long_min_2 = 20.9
2023-11-25 08:37:29,627 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_short_max_1 = 21.4
2023-11-25 08:37:29,627 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_short_max_2 = 50.8
2023-11-25 08:37:29,627 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_short_min_1 = 9.9
2023-11-25 08:37:29,627 - freqtrade.strategy.hyper - INFO - Strategy Parameter: adx_short_min_2 = 30.3
2023-11-25 08:37:29,627 - freqtrade.strategy.hyper - INFO - Strategy Parameter: bb_tp_l = 16
2023-11-25 08:37:29,627 - freqtrade.strategy.hyper - INFO - Strategy Parameter: bb_tp_s = 20
2023-11-25 08:37:29,628 - freqtrade.strategy.hyper - INFO - Strategy Parameter: leverage_num = 5
2023-11-25 08:37:29,628 - freqtrade.strategy.hyper - INFO - Strategy Parameter: rsi_tp_l = 22
2023-11-25 08:37:29,628 - freqtrade.strategy.hyper - INFO - Strategy Parameter: rsi_tp_s = 17
2023-11-25 08:37:29,628 - freqtrade.strategy.hyper - INFO - Strategy Parameter: volume_check = 38
2023-11-25 08:37:29,628 - freqtrade.strategy.hyper - INFO - Strategy Parameter: volume_check_s = 20
2023-11-25 08:37:29,629 - freqtrade.strategy.hyper - INFO - Strategy Parameter: atr_long_mul = 3.8
2023-11-25 08:37:29,629 - freqtrade.strategy.hyper - INFO - Strategy Parameter: atr_short_mul = 5.0
2023-11-25 08:37:29,629 - freqtrade.strategy.hyper - INFO - Strategy Parameter: ema_period_l_exit = 91
2023-11-25 08:37:29,629 - freqtrade.strategy.hyper - INFO - Strategy Parameter: ema_period_s_exit = 147
2023-11-25 08:37:29,629 - freqtrade.strategy.hyper - INFO - Strategy Parameter: volume_check_exit = 19
2023-11-25 08:37:29,630 - freqtrade.strategy.hyper - INFO - Strategy Parameter: volume_check_exit_s = 41
2023-11-25 08:37:29,630 - freqtrade.strategy.hyper - INFO - Strategy Parameter: max_allowed_drawdown = 0.1
2023-11-25 08:37:29,630 - freqtrade.strategy.hyper - INFO - Strategy Parameter: max_drawdown_lookback = 2
2023-11-25 08:37:29,631 - freqtrade.strategy.hyper - INFO - Strategy Parameter: max_drawdown_stop_duration = 4
2023-11-25 08:37:29,631 - freqtrade.strategy.hyper - INFO - Strategy Parameter: max_drawdown_trade_limit = 1
2023-11-25 08:37:29,631 - freqtrade.strategy.hyper - INFO - Strategy Parameter: stoploss_guard_lookback = 8
2023-11-25 08:37:29,631 - freqtrade.strategy.hyper - INFO - Strategy Parameter: stoploss_guard_stop_duration = 5
2023-11-25 08:37:29,631 - freqtrade.strategy.hyper - INFO - Strategy Parameter: stoploss_guard_trade_limit = 1
2023-11-25 08:37:38,085 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2021-01-02 06:00:00 up to 2023-10-27 00:00:00 (1027 days).
2023-11-25 10:02:06,946 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-11-25_10-02-06.meta.json"
2023-11-25 10:02:06,947 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2023-11-25_10-02-06.json"
2023-11-25 10:02:26,705 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy RSI_BB_MACD_Nov_2023_1h_2_Dec
================================================================= BACKTESTING REPORT =================================================================
|               Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |     Win  Draw  Loss  Win% |
|--------------------+-----------+----------------+----------------+-------------------+----------------+----------------+---------------------------|
|     UNFI/USDT:USDT |      3226 |           2.26 |        7292.11 |           721.571 |          72.16 |        2:26:00 |    2509     0   717  77.8 |
|      GRT/USDT:USDT |      3453 |           2.09 |        7226.34 |           716.318 |          71.63 |        2:36:00 |    2704     0   749  78.3 |
|      RSR/USDT:USDT |      3256 |           2.20 |        7162.47 |           715.875 |          71.59 |        2:29:00 |    2553     0   703  78.4 |
|      REN/USDT:USDT |      3263 |           2.11 |        6890.14 |           685.119 |          68.51 |        2:31:00 |    2546     0   717  78.0 |
|      SNX/USDT:USDT |      3356 |           2.02 |        6770.14 |           671.120 |          67.11 |        2:33:00 |    2618     0   738  78.0 |
|      SKL/USDT:USDT |      3311 |           1.96 |        6476.86 |           646.019 |          64.60 |        2:39:00 |    2580     0   731  77.9 |
|     RUNE/USDT:USDT |      3075 |           2.26 |        6934.67 |           644.814 |          64.48 |        2:21:00 |    2378     0   697  77.3 |
|      LRC/USDT:USDT |      3226 |           1.99 |        6430.36 |           638.170 |          63.82 |        2:52:00 |    2525     0   701  78.3 |
|     SAND/USDT:USDT |      3058 |           2.12 |        6481.46 |           635.967 |          63.60 |        2:45:00 |    2371     0   687  77.5 |
|      FTM/USDT:USDT |      3358 |           1.91 |        6398.87 |           633.541 |          63.35 |        2:25:00 |    2540     0   818  75.6 |
|      CRV/USDT:USDT |      3305 |           1.88 |        6224.88 |           621.106 |          62.11 |        2:26:00 |    2548     0   757  77.1 |
|    ALPHA/USDT:USDT |      3296 |           1.88 |        6185.56 |           612.503 |          61.25 |        2:38:00 |    2546     0   750  77.2 |
|      LIT/USDT:USDT |      3191 |           1.90 |        6052.85 |           602.815 |          60.28 |        2:39:00 |    2451     0   740  76.8 |
|     BAND/USDT:USDT |      3291 |           1.84 |        6044.31 |           599.571 |          59.96 |        2:46:00 |    2539     0   752  77.1 |
|      FLM/USDT:USDT |      3038 |           1.97 |        5992.69 |           596.820 |          59.68 |        2:51:00 |    2356     0   682  77.6 |
|      RLC/USDT:USDT |      3562 |           1.68 |        5987.65 |           596.782 |          59.68 |        2:34:00 |    2752     0   810  77.3 |
|    SUSHI/USDT:USDT |      3153 |           2.03 |        6407.03 |           595.518 |          59.55 |        2:41:00 |    2469     0   684  78.3 |
|      OGN/USDT:USDT |      3142 |           1.90 |        5985.27 |           593.591 |          59.36 |        2:40:00 |    2419     0   723  77.0 |
|      TRB/USDT:USDT |      3439 |           1.78 |        6126.77 |           588.904 |          58.89 |        2:24:00 |    2639     0   800  76.7 |
|     LINA/USDT:USDT |      3129 |           1.86 |        5834.55 |           583.175 |          58.32 |        2:20:00 |    2407     0   722  76.9 |
|      ONE/USDT:USDT |      3002 |           1.94 |        5836.59 |           582.896 |          58.29 |        2:44:00 |    2315     0   687  77.1 |
|     NEAR/USDT:USDT |      3029 |           2.05 |        6196.75 |           582.198 |          58.22 |        2:47:00 |    2319     0   710  76.6 |
|    OCEAN/USDT:USDT |      3291 |           1.76 |        5780.72 |           574.255 |          57.43 |        2:50:00 |    2540     0   751  77.2 |
|     DENT/USDT:USDT |      2673 |           2.14 |        5712.72 |           571.162 |          57.12 |        3:15:00 |    2100     0   573  78.6 |
|      OMG/USDT:USDT |      2920 |           1.96 |        5722.69 |           569.070 |          56.91 |        3:07:00 |    2306     0   614  79.0 |
|      KSM/USDT:USDT |      3253 |           2.03 |        6606.55 |           559.770 |          55.98 |        3:05:00 |    2585     0   668  79.5 |
|     ATOM/USDT:USDT |      3086 |           1.78 |        5479.28 |           546.575 |          54.66 |        3:02:00 |    2379     0   707  77.1 |
|      BLZ/USDT:USDT |      3446 |           1.58 |        5460.17 |           544.982 |          54.50 |        2:29:00 |    2625     0   821  76.2 |
|      NKN/USDT:USDT |      2953 |           1.83 |        5401.85 |           538.518 |          53.85 |        2:55:00 |    2295     0   658  77.7 |
|      ENJ/USDT:USDT |      3062 |           1.75 |        5368.40 |           528.669 |          52.87 |        3:10:00 |    2383     0   679  77.8 |
|     COMP/USDT:USDT |      3061 |           1.71 |        5249.31 |           523.423 |          52.34 |        2:57:00 |    2419     0   642  79.0 |
|      ZEN/USDT:USDT |      3128 |           1.78 |        5563.48 |           523.265 |          52.33 |        2:51:00 |    2458     0   670  78.6 |
|      GTC/USDT:USDT |      2726 |           1.92 |        5221.23 |           519.037 |          51.90 |        2:50:00 |    2126     0   600  78.0 |
|      KNC/USDT:USDT |      3219 |           1.64 |        5275.70 |           518.483 |          51.85 |        2:54:00 |    2492     0   727  77.4 |
|      CHR/USDT:USDT |      2996 |           1.73 |        5176.57 |           515.867 |          51.59 |        2:50:00 |    2320     0   676  77.4 |
|    ALICE/USDT:USDT |      2857 |           1.80 |        5147.82 |           509.013 |          50.90 |        2:44:00 |    2185     0   672  76.5 |
|     IOST/USDT:USDT |      2619 |           1.92 |        5017.34 |           501.478 |          50.15 |        3:48:00 |    2072     0   547  79.1 |
|      RVN/USDT:USDT |      2736 |           1.83 |        5002.68 |           499.792 |          49.98 |        3:28:00 |    2180     0   556  79.7 |
|      VET/USDT:USDT |      2899 |           1.72 |        4975.88 |           497.129 |          49.71 |        3:29:00 |    2247     0   652  77.5 |
|     MASK/USDT:USDT |      2440 |           2.15 |        5234.87 |           492.500 |          49.25 |        2:42:00 |    1922     0   518  78.8 |
|     DOGE/USDT:USDT |      2486 |           1.96 |        4871.03 |           486.274 |          48.63 |        3:57:00 |    1988     0   498  80.0 |
|     MANA/USDT:USDT |      2613 |           1.88 |        4924.28 |           484.402 |          48.44 |        3:16:00 |    2059     0   554  78.8 |
|     COTI/USDT:USDT |      2993 |           1.62 |        4846.24 |           483.101 |          48.31 |        2:57:00 |    2314     0   679  77.3 |
|     CELR/USDT:USDT |      2935 |           1.64 |        4825.87 |           482.240 |          48.22 |        2:45:00 |    2247     0   688  76.6 |
|      BEL/USDT:USDT |      3007 |           1.63 |        4899.86 |           481.331 |          48.13 |        2:45:00 |    2308     0   699  76.8 |
|      DGB/USDT:USDT |      2476 |           1.94 |        4815.62 |           481.297 |          48.13 |        3:56:00 |    1982     0   494  80.0 |
|     DYDX/USDT:USDT |      2463 |           1.97 |        4848.72 |           480.715 |          48.07 |        2:31:00 |    1887     0   576  76.6 |
|     GALA/USDT:USDT |      2195 |           2.19 |        4812.46 |           480.325 |          48.03 |        3:07:00 |    1725     0   470  78.6 |
|      MKR/USDT:USDT |      2868 |           1.70 |        4869.84 |           476.629 |          47.66 |        3:22:00 |    2258     0   610  78.7 |
|      HOT/USDT:USDT |      2480 |           1.92 |        4754.77 |           475.365 |          47.54 |        3:51:00 |    1990     0   490  80.2 |
|      SFP/USDT:USDT |      2916 |           1.65 |        4804.61 |           474.100 |          47.41 |        3:13:00 |    2251     0   665  77.2 |
|    1INCH/USDT:USDT |      2704 |           1.81 |        4882.90 |           473.839 |          47.38 |        3:28:00 |    2136     0   568  79.0 |
|    THETA/USDT:USDT |      2900 |           1.63 |        4726.50 |           470.219 |          47.02 |        3:11:00 |    2265     0   635  78.1 |
|      CHZ/USDT:USDT |      2931 |           1.59 |        4660.49 |           464.490 |          46.45 |        3:14:00 |    2255     0   676  76.9 |
|      CTK/USDT:USDT |      2967 |           1.58 |        4683.86 |           461.824 |          46.18 |        3:32:00 |    2311     0   656  77.9 |
|      ZEC/USDT:USDT |      2787 |           1.65 |        4594.33 |           458.651 |          45.87 |        3:44:00 |    2205     0   582  79.1 |
|      BAL/USDT:USDT |      2733 |           1.70 |        4650.00 |           455.008 |          45.50 |        3:22:00 |    2159     0   574  79.0 |
|      ZIL/USDT:USDT |      2898 |           1.57 |        4548.10 |           454.343 |          45.43 |        3:21:00 |    2266     0   632  78.2 |
|      NEO/USDT:USDT |      2688 |           1.68 |        4503.52 |           448.899 |          44.89 |        3:40:00 |    2137     0   551  79.5 |
|      ETC/USDT:USDT |      2537 |           1.78 |        4508.07 |           448.442 |          44.84 |        3:54:00 |    2018     0   519  79.5 |
|      ICX/USDT:USDT |      2874 |           1.58 |        4537.29 |           448.426 |          44.84 |        3:14:00 |    2215     0   659  77.1 |
|      SXP/USDT:USDT |      2765 |           1.61 |        4443.56 |           443.296 |          44.33 |        3:18:00 |    2137     0   628  77.3 |
|    WAVES/USDT:USDT |      2927 |           1.52 |        4453.87 |           439.658 |          43.97 |        3:10:00 |    2240     0   687  76.5 |
|     ANKR/USDT:USDT |      2850 |           1.53 |        4359.30 |           435.446 |          43.54 |        3:15:00 |    2215     0   635  77.7 |
|     KAVA/USDT:USDT |      2928 |           1.46 |        4283.53 |           426.852 |          42.69 |        3:22:00 |    2258     0   670  77.1 |
|     REEF/USDT:USDT |      2779 |           1.53 |        4247.60 |           424.608 |          42.46 |        3:11:00 |    2172     0   607  78.2 |
|     IOTA/USDT:USDT |      2723 |           1.53 |        4175.72 |           417.028 |          41.70 |        3:49:00 |    2133     0   590  78.3 |
|      XTZ/USDT:USDT |      2659 |           1.57 |        4164.83 |           414.663 |          41.47 |        3:42:00 |    2081     0   578  78.3 |
| 1000SHIB/USDT:USDT |      2295 |           1.80 |        4129.69 |           412.811 |          41.28 |        3:47:00 |    1792     0   503  78.1 |
|     EGLD/USDT:USDT |      2722 |           1.76 |        4787.94 |           412.755 |          41.28 |        3:39:00 |    2174     0   548  79.9 |
|     ALGO/USDT:USDT |      2896 |           1.42 |        4101.52 |           409.701 |          40.97 |        3:25:00 |    2232     0   664  77.1 |
|     HBAR/USDT:USDT |      2617 |           1.56 |        4086.09 |           407.704 |          40.77 |        3:34:00 |    2032     0   585  77.6 |
|     STMX/USDT:USDT |      2701 |           1.51 |        4072.42 |           407.087 |          40.71 |        3:15:00 |    2066     0   635  76.5 |
|      DOT/USDT:USDT |      2581 |           1.61 |        4146.18 |           405.102 |          40.51 |        3:53:00 |    1985     0   596  76.9 |
|     LINK/USDT:USDT |      2644 |           1.54 |        4060.39 |           405.081 |          40.51 |        3:18:00 |    2069     0   575  78.3 |
|       AR/USDT:USDT |      2154 |           1.93 |        4160.49 |           404.596 |          40.46 |        3:20:00 |    1730     0   424  80.3 |
|     AAVE/USDT:USDT |      2999 |           1.60 |        4783.60 |           403.968 |          40.40 |        3:01:00 |    2371     0   628  79.1 |
|      AXS/USDT:USDT |      2456 |           1.78 |        4380.37 |           400.904 |          40.09 |        2:56:00 |    1885     0   571  76.8 |
|      XEM/USDT:USDT |      2284 |           1.74 |        3982.84 |           397.476 |          39.75 |        4:23:00 |    1773     0   511  77.6 |
|    MATIC/USDT:USDT |      2927 |           1.37 |        4005.36 |           396.066 |          39.61 |        3:10:00 |    2215     0   712  75.7 |
|      C98/USDT:USDT |      2328 |           1.72 |        4002.61 |           395.223 |          39.52 |        3:10:00 |    1810     0   518  77.7 |
|      YFI/USDT:USDT |      2775 |           1.69 |        4683.08 |           390.902 |          39.09 |        3:49:00 |    2222     0   553  80.1 |
|      UNI/USDT:USDT |      2879 |           1.62 |        4676.37 |           388.963 |          38.90 |        3:20:00 |    2250     0   629  78.2 |
|     BAKE/USDT:USDT |      2721 |           1.43 |        3895.81 |           384.634 |          38.46 |        2:50:00 |    2086     0   635  76.7 |
|    STORJ/USDT:USDT |      3002 |           1.29 |        3858.54 |           380.683 |          38.07 |        3:04:00 |    2272     0   730  75.7 |
|     QTUM/USDT:USDT |      2644 |           1.45 |        3838.15 |           380.305 |          38.03 |        3:45:00 |    2068     0   576  78.2 |
|      ATA/USDT:USDT |      2154 |           1.77 |        3809.80 |           379.715 |          37.97 |        3:27:00 |    1676     0   478  77.8 |
|   PEOPLE/USDT:USDT |      1907 |           1.97 |        3763.20 |           376.130 |          37.61 |        3:14:00 |    1474     0   433  77.3 |
|       OP/USDT:USDT |      1579 |           2.38 |        3760.69 |           375.465 |          37.55 |        2:44:00 |    1265     0   314  80.1 |
|      XRP/USDT:USDT |      2205 |           1.70 |        3742.20 |           373.812 |          37.38 |        4:39:00 |    1737     0   468  78.8 |
|      FIL/USDT:USDT |      2552 |           1.53 |        3915.37 |           368.378 |          36.84 |        3:39:00 |    2038     0   514  79.9 |
|      BAT/USDT:USDT |      2743 |           1.34 |        3669.69 |           366.615 |          36.66 |        3:32:00 |    2130     0   613  77.7 |
|     CELO/USDT:USDT |      2052 |           1.76 |        3613.29 |           360.467 |          36.05 |        3:28:00 |    1607     0   445  78.3 |
|      MTL/USDT:USDT |      2553 |           1.44 |        3674.13 |           357.914 |          35.79 |        3:28:00 |    1954     0   599  76.5 |
|    AUDIO/USDT:USDT |      2157 |           1.66 |        3585.98 |           354.075 |          35.41 |        3:19:00 |    1687     0   470  78.2 |
|      EOS/USDT:USDT |      2328 |           1.50 |        3482.72 |           346.989 |          34.70 |        4:10:00 |    1848     0   480  79.4 |
|      XLM/USDT:USDT |      2449 |           1.40 |        3440.68 |           342.896 |          34.29 |        4:24:00 |    1963     0   486  80.2 |
|      ONT/USDT:USDT |      2659 |           1.29 |        3419.20 |           341.561 |          34.16 |        3:43:00 |    2085     0   574  78.4 |
|      LTC/USDT:USDT |      2420 |           1.41 |        3404.85 |           339.914 |          33.99 |        4:10:00 |    1921     0   499  79.4 |
|     DASH/USDT:USDT |      2553 |           1.31 |        3354.29 |           334.875 |          33.49 |        4:03:00 |    1992     0   561  78.0 |
|      ADA/USDT:USDT |      2363 |           1.43 |        3372.94 |           333.149 |          33.31 |        4:27:00 |    1863     0   500  78.8 |
|      SOL/USDT:USDT |      2218 |           1.74 |        3855.78 |           331.889 |          33.19 |        2:43:00 |    1712     0   506  77.2 |
|      ZRX/USDT:USDT |      2776 |           1.19 |        3313.32 |           330.853 |          33.09 |        3:24:00 |    2157     0   619  77.7 |
|      ANT/USDT:USDT |      1895 |           1.75 |        3323.30 |           330.768 |          33.08 |        3:25:00 |    1502     0   393  79.3 |
|      ENS/USDT:USDT |      2050 |           1.65 |        3379.67 |           329.661 |          32.97 |        3:25:00 |    1605     0   445  78.3 |
|     IOTX/USDT:USDT |      2063 |           1.59 |        3279.07 |           327.673 |          32.77 |        3:49:00 |    1625     0   438  78.8 |
|      LPT/USDT:USDT |      1925 |           1.69 |        3246.09 |           320.774 |          32.08 |        3:33:00 |    1546     0   379  80.3 |
|     CTSI/USDT:USDT |      1982 |           1.62 |        3203.26 |           319.061 |          31.91 |        3:35:00 |    1581     0   401  79.8 |
|     ROSE/USDT:USDT |      1753 |           1.80 |        3150.05 |           314.325 |          31.43 |        3:51:00 |    1403     0   350  80.0 |
|     DUSK/USDT:USDT |      1640 |           1.86 |        3055.75 |           304.621 |          30.46 |        3:39:00 |    1302     0   338  79.4 |
|      ETH/USDT:USDT |      1973 |           1.44 |        2850.90 |           277.716 |          27.77 |        5:16:00 |    1593     0   380  80.7 |
|      BCH/USDT:USDT |      2236 |           1.25 |        2784.75 |           277.214 |          27.72 |        4:48:00 |    1767     0   469  79.0 |
|      IMX/USDT:USDT |      1828 |           1.52 |        2781.01 |           275.138 |          27.51 |        3:09:00 |    1410     0   418  77.1 |
|      GMT/USDT:USDT |      1607 |           1.70 |        2737.02 |           270.520 |          27.05 |        3:33:00 |    1227     0   380  76.4 |
|      WOO/USDT:USDT |      1545 |           1.75 |        2698.94 |           269.270 |          26.93 |        3:24:00 |    1226     0   319  79.4 |
|      XMR/USDT:USDT |      2228 |           1.21 |        2699.65 |           269.268 |          26.93 |        5:55:00 |    1775     0   453  79.7 |
|     API3/USDT:USDT |      1700 |           1.57 |        2668.76 |           266.083 |          26.61 |        3:33:00 |    1337     0   363  78.6 |
|     FLOW/USDT:USDT |      1494 |           1.75 |        2620.58 |           261.459 |          26.15 |        4:21:00 |    1214     0   280  81.3 |
|     AVAX/USDT:USDT |      2325 |           1.40 |        3264.26 |           254.494 |          25.45 |        2:59:00 |    1782     0   543  76.6 |
|      APE/USDT:USDT |      1549 |           1.71 |        2648.57 |           250.640 |          25.06 |        3:40:00 |    1205     0   344  77.8 |
|     ARPA/USDT:USDT |      1785 |           1.37 |        2451.73 |           244.987 |          24.50 |        4:18:00 |    1409     0   376  78.9 |
|     KLAY/USDT:USDT |      1472 |           1.65 |        2435.27 |           243.364 |          24.34 |        5:42:00 |    1223     0   249  83.1 |
|      GAL/USDT:USDT |      1470 |           1.69 |        2483.06 |           241.220 |          24.12 |        3:38:00 |    1152     0   318  78.4 |
|  1000XEC/USDT:USDT |      1705 |           1.39 |        2362.43 |           235.939 |          23.59 |        4:53:00 |    1377     0   328  80.8 |
|      BNX/USDT:USDT |       558 |           1.77 |         990.26 |            98.949 |           9.89 |        4:06:00 |     448     1   109  80.3 |
|      ICP/USDT:USDT |       787 |           1.26 |         992.13 |            93.610 |           9.36 |        5:19:00 |     647     0   140  82.2 |
|      TRX/USDT:USDT |      1785 |           0.34 |         603.74 |            60.294 |           6.03 |        7:25:00 |    1372     0   413  76.9 |
|      TLM/USDT:USDT |       329 |           0.62 |         203.74 |            20.368 |           2.04 |        8:03:00 |     270     0    59  82.1 |
|      BTC/USDT:USDT |         0 |           0.00 |           0.00 |             0.000 |           0.00 |           0:00 |       0     0     0     0 |
|              TOTAL |    330583 |           1.72 |      567775.90 |         55624.931 |        5562.49 |        3:18:00 | 258069     1  72513  78.1 |

============================================================ ENTER TAG STATS ============================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |     Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+---------------------------|
| TOTAL |    330583 |           1.72 |      567775.90 |         55624.931 |        5562.49 |        3:18:00 | 258069     1  72513  78.1 |
======================================================== EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |    Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+---------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |  276548 | 230159     0  46389  83.2 |           3.28 |      906144    |         88932.8   |        7024.37 |
|                roi |   28596 |   27906     1   689  97.6 |          15.58 |      445581    |         43651.2   |        3454.12 |
|          stop_loss |   23505 |      0     0  23505     0 |         -31.78 |     -747019    |        -73325.2   |       -5790.85 |
|         exit_short |    1567 |       4     0  1563   0.3 |         -19.15 |      -30007    |         -2950.15  |        -232.61 |
|          exit_long |     289 |       0     0   289     0 |         -21.26 |       -6142.89 |          -606.171 |         -47.62 |
|         force_exit |      78 |       0     0    78     0 |         -10    |        -780.26 |           -77.546 |          -6.05 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |          1907.76  |   7487 |       0 |     2798 |
| 28/02/2021 |          2654.07  |   7194 |       0 |     2495 |
| 31/03/2021 |          1488.02  |   7513 |       0 |     2577 |
| 30/04/2021 |          2919.28  |   9757 |       0 |     3353 |
| 31/05/2021 |          4652.28  |  10344 |       0 |     3332 |
| 30/06/2021 |          2228.95  |   8684 |       0 |     2780 |
| 31/07/2021 |          1398.2   |   7920 |       0 |     2446 |
| 31/08/2021 |          1695.4   |   8765 |       0 |     2969 |
| 30/09/2021 |          2319.05  |   8064 |       0 |     2298 |
| 31/10/2021 |           933.551 |   7900 |       0 |     2373 |
| 30/11/2021 |          2016.53  |   7780 |       0 |     2219 |
| 31/12/2021 |          2135.12  |   8329 |       0 |     2301 |
| 31/01/2022 |          1409.27  |   7330 |       0 |     2136 |
| 28/02/2022 |          1787.02  |   7100 |       0 |     1915 |
| 31/03/2022 |          1004.36  |   8426 |       0 |     2446 |
| 30/04/2022 |          2775.61  |   8715 |       0 |     1913 |
| 31/05/2022 |          3004.06  |  11765 |       0 |     4338 |
| 30/06/2022 |          3191.42  |  11684 |       0 |     3857 |
| 31/07/2022 |           695.469 |   8201 |       0 |     2396 |
| 31/08/2022 |          1291.48  |   7442 |       0 |     1963 |
| 30/09/2022 |           874.204 |   7234 |       0 |     1930 |
| 31/10/2022 |           918.58  |   5719 |       0 |     1073 |
| 30/11/2022 |          1989.34  |   7572 |       0 |     1859 |
| 31/12/2022 |          1579.76  |   5865 |       0 |      815 |
| 31/01/2023 |           166.268 |   6951 |       0 |     2319 |
| 28/02/2023 |          1577.26  |   7008 |       0 |     1690 |
| 31/03/2023 |          1590.42  |   8421 |       0 |     2083 |
| 30/04/2023 |           507.111 |   5962 |       0 |     1281 |
| 31/05/2023 |          1003.21  |   5379 |       0 |      812 |
| 30/06/2023 |          1129.07  |   6320 |       0 |     1404 |
| 31/07/2023 |          1207.74  |   7107 |       0 |     1436 |
| 31/08/2023 |          1143.13  |   5610 |       0 |      793 |
| 30/09/2023 |           297.51  |   4594 |       1 |      977 |
| 31/10/2023 |           134.429 |   3927 |       0 |     1136 |
===================== SUMMARY METRICS =====================
| Metric                      | Value                     |
|-----------------------------+---------------------------|
| Backtesting from            | 2021-01-02 06:00:00       |
| Backtesting to              | 2023-10-27 00:00:00       |
| Max open trades             | 129                       |
|                             |                           |
| Total/Daily Avg Trades      | 330583 / 321.89           |
| Starting balance            | 1000 USDT                 |
| Final balance               | 56624.931 USDT            |
| Absolute profit             | 55624.931 USDT            |
| Total profit %              | 5562.49%                  |
| CAGR %                      | 319.78%                   |
| Sortino                     | 803.48                    |
| Sharpe                      | 933.98                    |
| Calmar                      | 7713.77                   |
| Profit factor               | 1.55                      |
| Expectancy (Ratio)          | 0.17 (0.12)               |
| Trades per day              | 321.89                    |
| Avg. daily profit %         | 5.42%                     |
| Avg. stake amount           | 9.819 USDT                |
| Total trade volume          | 3246141.976 USDT          |
|                             |                           |
| Long / Short                | 35683 / 294900            |
| Total profit Long %         | 605.20%                   |
| Total profit Short %        | 4957.29%                  |
| Absolute profit Long        | 6052.032 USDT             |
| Absolute profit Short       | 49572.899 USDT            |
|                             |                           |
| Best Pair                   | UNFI/USDT:USDT 7292.11%   |
| Worst Pair                  | BTC/USDT:USDT 0.00%       |
| Best trade                  | TRB/USDT:USDT 28.71%      |
| Worst trade                 | 1000XEC/USDT:USDT -52.48% |
| Best day                    | 706.655 USDT              |
| Worst day                   | -278.428 USDT             |
| Days win/draw/lose          | 775 / 0 / 254             |
| Avg. Duration Winners       | 2:42:00                   |
| Avg. Duration Loser         | 5:27:00                   |
| Max Consecutive Wins / Loss | 221 / 78                  |
| Rejected Entry signals      | 0                         |
| Entry/Exit Timeouts         | 0 / 160164                |
|                             |                           |
| Min balance                 | 1000.98 USDT              |
| Max balance                 | 56798.515 USDT            |
| Max % of account underwater | 11.65%                    |
| Absolute Drawdown (Account) | 1.34%                     |
| Absolute Drawdown           | 642.314 USDT              |
| Drawdown high               | 46881.613 USDT            |
| Drawdown low                | 46239.299 USDT            |
| Drawdown Start              | 2023-01-01 16:00:00       |
| Drawdown End                | 2023-01-16 07:00:00       |
| Market change               | 37.70%                    |
===========================================================

Backtested 2021-01-02 06:00:00 -> 2023-10-27 00:00:00 | Max open trades : 129
================================================================================= STRATEGY SUMMARY ================================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |     Win  Draw  Loss  Win% |            Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+---------------------------+---------------------|
| RSI_BB_MACD_Nov_2023_1h_2_Dec|    330583 |           1.72 |      567775.90 |         55624.931 |        5562.49 |        3:18:00 | 258069     1  72513  78.1 | 642.314 USDT  1.34% |
===================================================================================================================================================================================







(((((same config but with 4 max open trades and 200 USDt per trade)))))





Result for strategy RSI_BB_MACD_Nov_2023_1h_2_Dec
================================================================ BACKTESTING REPORT ================================================================
|               Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|--------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
|      OMG/USDT:USDT |      2484 |           1.83 |        4557.57 |          9111.170 |         911.12 |        2:54:00 |  1921     0   563  77.3 |
|      HOT/USDT:USDT |      1598 |           2.40 |        3829.11 |          7656.991 |         765.70 |        2:55:00 |  1281     0   317  80.2 |
|      XTZ/USDT:USDT |      2208 |           1.66 |        3662.09 |          7321.328 |         732.13 |        3:26:00 |  1708     0   500  77.4 |
|     IOTX/USDT:USDT |      1832 |           1.66 |        3034.12 |          6066.986 |         606.70 |        3:43:00 |  1439     0   393  78.5 |
|      BAL/USDT:USDT |      1567 |           1.84 |        2887.63 |          5767.044 |         576.70 |        2:38:00 |  1197     0   370  76.4 |
|      SXP/USDT:USDT |      1393 |           2.00 |        2786.71 |          5571.787 |         557.18 |        2:17:00 |  1039     0   354  74.6 |
|      KSM/USDT:USDT |      1275 |           2.18 |        2775.17 |          5475.166 |         547.52 |        2:15:00 |   984     0   291  77.2 |
|     QTUM/USDT:USDT |      1067 |           1.93 |        2063.69 |          4124.569 |         412.46 |        2:32:00 |   813     0   254  76.2 |
|  1000XEC/USDT:USDT |      1520 |           1.34 |        2032.46 |          4063.953 |         406.40 |        4:56:00 |  1223     0   297  80.5 |
|     API3/USDT:USDT |      1016 |           1.75 |        1773.71 |          3546.373 |         354.64 |        3:07:00 |   802     0   214  78.9 |
|      GRT/USDT:USDT |       629 |           2.61 |        1642.55 |          3282.992 |         328.30 |        1:46:00 |   476     0   153  75.7 |
|     ATOM/USDT:USDT |       832 |           1.81 |        1505.14 |          3009.653 |         300.97 |        2:33:00 |   607     0   225  73.0 |
|     COTI/USDT:USDT |       466 |           2.58 |        1203.95 |          2407.216 |         240.72 |        2:19:00 |   364     0   102  78.1 |
|      FIL/USDT:USDT |       594 |           1.48 |         877.13 |          1750.709 |         175.07 |        3:21:00 |   453     0   141  76.3 |
|      RLC/USDT:USDT |       400 |           1.98 |         791.69 |          1582.837 |         158.28 |        1:32:00 |   293     0   107  73.2 |
|      SKL/USDT:USDT |       210 |           3.73 |         784.23 |          1567.885 |         156.79 |        1:35:00 |   166     0    44  79.0 |
|     ALGO/USDT:USDT |       261 |           2.72 |         710.90 |          1421.616 |         142.16 |        2:08:00 |   200     0    61  76.6 |
|      RVN/USDT:USDT |       376 |           1.49 |         561.83 |          1123.406 |         112.34 |        1:57:00 |   287     0    89  76.3 |
|      XMR/USDT:USDT |       274 |           1.96 |         538.32 |          1076.418 |         107.64 |        5:32:00 |   214     0    60  78.1 |
|      MTL/USDT:USDT |       290 |           1.86 |         538.45 |          1075.448 |         107.54 |        2:38:00 |   209     0    81  72.1 |
|      NEO/USDT:USDT |       256 |           2.01 |         514.33 |          1028.388 |         102.84 |        2:19:00 |   190     0    66  74.2 |
|    STORJ/USDT:USDT |       174 |           2.95 |         513.13 |          1025.499 |         102.55 |        2:05:00 |   130     0    44  74.7 |
|      ADA/USDT:USDT |       294 |           1.56 |         458.10 |           915.486 |          91.55 |        4:24:00 |   223     0    71  75.9 |
|      SFP/USDT:USDT |       159 |           2.61 |         414.50 |           828.270 |          82.83 |        3:37:00 |   128     0    31  80.5 |
|      OGN/USDT:USDT |        89 |           4.20 |         374.05 |           747.662 |          74.77 |        1:06:00 |    71     0    18  79.8 |
|      LPT/USDT:USDT |       259 |           1.34 |         347.08 |           693.333 |          69.33 |        3:05:00 |   198     0    61  76.4 |
|     NEAR/USDT:USDT |        98 |           3.55 |         347.65 |           692.361 |          69.24 |        1:12:00 |    76     0    22  77.6 |
|      DGB/USDT:USDT |       181 |           1.65 |         298.97 |           597.836 |          59.78 |        4:17:00 |   142     0    39  78.5 |
|      ZIL/USDT:USDT |        72 |           3.84 |         276.52 |           552.946 |          55.29 |        1:04:00 |    59     0    13  81.9 |
|      KNC/USDT:USDT |        85 |           2.93 |         248.75 |           497.063 |          49.71 |        2:03:00 |    63     0    22  74.1 |
|      BTC/USDT:USDT |        50 |           4.86 |         242.79 |           477.855 |          47.79 |        2:50:00 |    45     0     5  90.0 |
|     AVAX/USDT:USDT |        56 |           4.30 |         240.92 |           476.654 |          47.67 |        0:44:00 |    42     0    14  75.0 |
|     CELR/USDT:USDT |        51 |           4.41 |         224.69 |           449.341 |          44.93 |        1:13:00 |    42     0     9  82.4 |
|     IOST/USDT:USDT |        31 |           7.04 |         218.32 |           436.604 |          43.66 |        2:56:00 |    27     0     4  87.1 |
|      SOL/USDT:USDT |       108 |           1.98 |         213.78 |           416.985 |          41.70 |        1:21:00 |    77     0    31  71.3 |
|      APE/USDT:USDT |       139 |           1.49 |         207.18 |           412.846 |          41.28 |        3:06:00 |    99     0    40  71.2 |
|     MASK/USDT:USDT |        42 |           4.43 |         186.01 |           370.302 |          37.03 |        0:56:00 |    33     0     9  78.6 |
|     CTSI/USDT:USDT |        76 |           2.42 |         183.88 |           367.653 |          36.77 |        1:48:00 |    57     0    19  75.0 |
|      DOT/USDT:USDT |        89 |           1.92 |         171.08 |           341.555 |          34.16 |        2:16:00 |    64     0    25  71.9 |
|     DYDX/USDT:USDT |        73 |           2.33 |         170.41 |           340.662 |          34.07 |        0:53:00 |    55     0    18  75.3 |
|      IMX/USDT:USDT |       132 |           1.28 |         169.52 |           338.788 |          33.88 |        2:54:00 |    96     0    36  72.7 |
|      ZEN/USDT:USDT |        46 |           3.70 |         170.27 |           337.446 |          33.74 |        0:31:00 |    35     0    11  76.1 |
|    1INCH/USDT:USDT |        31 |           4.82 |         149.44 |           298.584 |          29.86 |        2:14:00 |    24     0     7  77.4 |
|     ROSE/USDT:USDT |        77 |           1.93 |         148.76 |           297.337 |          29.73 |        2:50:00 |    59     0    18  76.6 |
|    ALICE/USDT:USDT |        54 |           2.73 |         147.65 |           295.017 |          29.50 |        1:22:00 |    38     0    16  70.4 |
|      CRV/USDT:USDT |       112 |           1.25 |         140.10 |           280.166 |          28.02 |        1:14:00 |    80     0    32  71.4 |
|     KAVA/USDT:USDT |        76 |           1.82 |         138.33 |           276.583 |          27.66 |        3:36:00 |    59     0    17  77.6 |
|       OP/USDT:USDT |        23 |           5.96 |         137.15 |           274.221 |          27.42 |        2:31:00 |    21     0     2  91.3 |
|    SUSHI/USDT:USDT |        24 |           5.65 |         135.56 |           270.583 |          27.06 |        2:38:00 |    20     0     4  83.3 |
|      ETC/USDT:USDT |        38 |           3.34 |         127.11 |           254.152 |          25.42 |        2:57:00 |    31     0     7  81.6 |
|     DUSK/USDT:USDT |        22 |           5.50 |         120.94 |           241.824 |          24.18 |        2:08:00 |    18     0     4  81.8 |
|     IOTA/USDT:USDT |        56 |           2.07 |         116.11 |           232.180 |          23.22 |        2:32:00 |    42     0    14  75.0 |
|      LIT/USDT:USDT |       100 |           1.02 |         101.92 |           203.720 |          20.37 |        2:08:00 |    71     0    29  71.0 |
|      TLM/USDT:USDT |       100 |           1.00 |         100.33 |           200.631 |          20.06 |       10:00:00 |    85     0    15  85.0 |
|     MANA/USDT:USDT |        24 |           4.18 |         100.30 |           200.290 |          20.03 |        1:10:00 |    19     0     5  79.2 |
|     DASH/USDT:USDT |        33 |           2.94 |          97.16 |           194.271 |          19.43 |        1:44:00 |    23     0    10  69.7 |
|    AUDIO/USDT:USDT |        53 |           1.80 |          95.52 |           190.782 |          19.08 |        3:00:00 |    42     0    11  79.2 |
|    ALPHA/USDT:USDT |        18 |           5.29 |          95.19 |           190.265 |          19.03 |        0:30:00 |    15     0     3  83.3 |
|      ANT/USDT:USDT |        19 |           4.71 |          89.50 |           178.925 |          17.89 |        0:44:00 |    16     0     3  84.2 |
|     REEF/USDT:USDT |        17 |           5.23 |          88.93 |           177.860 |          17.79 |        3:39:00 |    15     0     2  88.2 |
|    MATIC/USDT:USDT |        11 |           7.55 |          83.02 |           165.963 |          16.60 |        0:33:00 |     9     0     2  81.8 |
|    WAVES/USDT:USDT |        73 |           1.10 |          80.65 |           161.351 |          16.14 |        1:32:00 |    51     0    22  69.9 |
|      XRP/USDT:USDT |        48 |           1.67 |          79.95 |           159.875 |          15.99 |        4:05:00 |    38     0    10  79.2 |
|      SNX/USDT:USDT |        12 |           6.56 |          78.72 |           157.360 |          15.74 |        0:25:00 |    11     0     1  91.7 |
|      AXS/USDT:USDT |        50 |           1.58 |          79.17 |           155.807 |          15.58 |        0:46:00 |    35     0    15  70.0 |
|      GMT/USDT:USDT |        12 |           5.40 |          64.76 |           129.440 |          12.94 |        1:00:00 |    10     0     2  83.3 |
|      ZEC/USDT:USDT |        20 |           3.03 |          60.50 |           120.958 |          12.10 |        2:12:00 |    16     0     4  80.0 |
|      GTC/USDT:USDT |         9 |           6.62 |          59.58 |           119.133 |          11.91 |        0:33:00 |     8     0     1  88.9 |
|     SAND/USDT:USDT |        18 |           3.13 |          56.37 |           112.767 |          11.28 |        0:33:00 |    13     0     5  72.2 |
|     DENT/USDT:USDT |         3 |          18.40 |          55.20 |           110.400 |          11.04 |        0:00:00 |     3     0     0   100 |
|      WOO/USDT:USDT |        12 |           4.43 |          53.21 |           106.397 |          10.64 |        1:35:00 |    11     0     1  91.7 |
|     EGLD/USDT:USDT |        12 |           4.30 |          51.57 |           102.720 |          10.27 |        1:25:00 |     9     0     3  75.0 |
|    OCEAN/USDT:USDT |        19 |           2.64 |          50.09 |           100.127 |          10.01 |        0:54:00 |    13     0     6  68.4 |
|      YFI/USDT:USDT |        23 |           2.17 |          49.97 |            98.899 |           9.89 |        0:57:00 |    15     0     8  65.2 |
|      RSR/USDT:USDT |        11 |           4.08 |          44.91 |            89.853 |           8.99 |        0:33:00 |    10     0     1  90.9 |
|      FLM/USDT:USDT |        18 |           2.49 |          44.90 |            89.788 |           8.98 |        1:43:00 |    12     0     6  66.7 |
|      BLZ/USDT:USDT |        80 |           0.56 |          44.57 |            89.123 |           8.91 |        1:20:00 |    55     0    25  68.8 |
|      ICX/USDT:USDT |        11 |           3.84 |          42.22 |            84.399 |           8.44 |        1:00:00 |     9     0     2  81.8 |
|      LRC/USDT:USDT |         4 |           9.72 |          38.87 |            77.698 |           7.77 |        1:30:00 |     3     0     1  75.0 |
|   PEOPLE/USDT:USDT |        14 |           2.75 |          38.55 |            77.082 |           7.71 |        0:39:00 |     9     0     5  64.3 |
|     ANKR/USDT:USDT |         4 |           9.56 |          38.24 |            76.464 |           7.65 |        9:45:00 |     4     0     0   100 |
|     KLAY/USDT:USDT |        11 |           3.47 |          38.22 |            76.417 |           7.64 |        5:38:00 |     9     0     2  81.8 |
|    THETA/USDT:USDT |         7 |           4.31 |          30.18 |            60.332 |           6.03 |        0:51:00 |     6     0     1  85.7 |
|      NKN/USDT:USDT |         8 |           3.74 |          29.96 |            59.897 |           5.99 |        8:22:00 |     5     0     3  62.5 |
|      XLM/USDT:USDT |        21 |           1.38 |          28.92 |            57.840 |           5.78 |        1:57:00 |    17     0     4  81.0 |
|     UNFI/USDT:USDT |        49 |           0.50 |          24.34 |            48.664 |           4.87 |        0:23:00 |    33     0    16  67.3 |
|      EOS/USDT:USDT |         6 |           4.06 |          24.36 |            48.663 |           4.87 |        1:00:00 |     5     0     1  83.3 |
| 1000SHIB/USDT:USDT |        15 |           1.58 |          23.70 |            47.380 |           4.74 |        0:28:00 |    10     0     5  66.7 |
|      BNX/USDT:USDT |         4 |           5.84 |          23.37 |            46.726 |           4.67 |        9:15:00 |     3     0     1  75.0 |
|      MKR/USDT:USDT |        38 |           0.60 |          22.88 |            45.735 |           4.57 |        2:36:00 |    28     0    10  73.7 |
|     ARPA/USDT:USDT |        13 |           1.67 |          21.67 |            43.337 |           4.33 |        1:55:00 |     9     0     4  69.2 |
|      TRX/USDT:USDT |        26 |           0.79 |          20.58 |            41.181 |           4.12 |        3:23:00 |    19     0     7  73.1 |
|      GAL/USDT:USDT |        11 |           1.67 |          18.36 |            36.574 |           3.66 |        4:00:00 |     8     0     3  72.7 |
|     LINK/USDT:USDT |        11 |           1.53 |          16.84 |            33.679 |           3.37 |        1:05:00 |     7     0     4  63.6 |
|      FTM/USDT:USDT |        18 |           0.84 |          15.11 |            30.184 |           3.02 |        0:47:00 |    13     0     5  72.2 |
|     BAKE/USDT:USDT |         3 |           4.78 |          14.33 |            28.576 |           2.86 |        1:00:00 |     2     0     1  66.7 |
|      XEM/USDT:USDT |        20 |           0.61 |          12.23 |            24.432 |           2.44 |        8:54:00 |    16     0     4  80.0 |
|     STMX/USDT:USDT |         8 |           1.39 |          11.13 |            22.243 |           2.22 |        1:15:00 |     4     0     4  50.0 |
|      BEL/USDT:USDT |         7 |           1.38 |           9.63 |            19.232 |           1.92 |        0:26:00 |     5     0     2  71.4 |
|      TRB/USDT:USDT |        27 |           0.29 |           7.80 |            15.402 |           1.54 |        1:36:00 |    19     0     8  70.4 |
|      ICP/USDT:USDT |         1 |           3.94 |           3.94 |             7.885 |           0.79 |        1:00:00 |     1     0     0   100 |
|      BAT/USDT:USDT |        20 |           0.09 |           1.82 |             3.596 |           0.36 |        4:45:00 |    13     0     7  65.0 |
|      UNI/USDT:USDT |         0 |           0.00 |           0.00 |             0.000 |           0.00 |           0:00 |     0     0     0     0 |
|      C98/USDT:USDT |         0 |           0.00 |           0.00 |             0.000 |           0.00 |           0:00 |     0     0     0     0 |
|      VET/USDT:USDT |        26 |          -0.04 |          -1.07 |            -2.135 |          -0.21 |        2:02:00 |    16     0    10  61.5 |
|      LTC/USDT:USDT |         2 |          -1.29 |          -2.58 |            -5.164 |          -0.52 |        1:00:00 |     1     0     1  50.0 |
|      ONE/USDT:USDT |        23 |          -0.15 |          -3.35 |            -6.667 |          -0.67 |        0:34:00 |    13     0    10  56.5 |
|     COMP/USDT:USDT |        15 |          -0.22 |          -3.35 |            -6.673 |          -0.67 |        0:44:00 |    10     0     5  66.7 |
|      ETH/USDT:USDT |         8 |          -0.63 |          -5.06 |           -10.150 |          -1.01 |        2:22:00 |     6     0     2  75.0 |
|      CHR/USDT:USDT |         7 |          -1.05 |          -7.34 |           -14.704 |          -1.47 |        0:43:00 |     5     0     2  71.4 |
|     DOGE/USDT:USDT |        20 |          -0.77 |         -15.48 |           -30.936 |          -3.09 |        0:24:00 |    11     0     9  55.0 |
|     LINA/USDT:USDT |         7 |          -2.55 |         -17.86 |           -35.704 |          -3.57 |        3:09:00 |     5     0     2  71.4 |
|     RUNE/USDT:USDT |        23 |          -0.85 |         -19.61 |           -39.347 |          -3.93 |        1:03:00 |    16     0     7  69.6 |
|      ZRX/USDT:USDT |        45 |          -0.46 |         -20.68 |           -41.331 |          -4.13 |        3:15:00 |    31     0    14  68.9 |
|      ATA/USDT:USDT |        39 |          -0.55 |         -21.32 |           -42.505 |          -4.25 |        1:28:00 |    29     0    10  74.4 |
|     FLOW/USDT:USDT |        32 |          -0.69 |         -22.13 |           -44.277 |          -4.43 |        5:47:00 |    25     0     7  78.1 |
|      BCH/USDT:USDT |         4 |          -7.08 |         -28.32 |           -56.583 |          -5.66 |        7:00:00 |     2     0     2  50.0 |
|     CELO/USDT:USDT |        22 |          -1.53 |         -33.61 |           -67.208 |          -6.72 |        1:00:00 |    15     0     7  68.2 |
|       AR/USDT:USDT |        23 |          -1.62 |         -37.23 |           -74.582 |          -7.46 |        1:39:00 |    13     0    10  56.5 |
|     BAND/USDT:USDT |        18 |          -2.10 |         -37.73 |           -75.420 |          -7.54 |        0:23:00 |    11     0     7  61.1 |
|      ONT/USDT:USDT |         5 |          -8.26 |         -41.30 |           -82.555 |          -8.26 |        3:12:00 |     3     0     2  60.0 |
|     GALA/USDT:USDT |         9 |          -4.60 |         -41.37 |           -82.725 |          -8.27 |        0:47:00 |     6     0     3  66.7 |
|     HBAR/USDT:USDT |        19 |          -2.38 |         -45.30 |           -90.568 |          -9.06 |        2:22:00 |    12     0     7  63.2 |
|      CTK/USDT:USDT |        53 |          -0.89 |         -46.91 |           -93.655 |          -9.37 |        2:28:00 |    37     0    16  69.8 |
|      REN/USDT:USDT |         8 |          -5.88 |         -47.06 |           -94.086 |          -9.41 |        1:00:00 |     5     0     3  62.5 |
|     AAVE/USDT:USDT |         7 |          -8.31 |         -58.20 |          -115.092 |         -11.51 |        8:43:00 |     4     0     3  57.1 |
|      ENS/USDT:USDT |         6 |         -11.01 |         -66.03 |          -131.905 |         -13.19 |        1:10:00 |     1     0     5  16.7 |
|      CHZ/USDT:USDT |         6 |         -15.46 |         -92.79 |          -185.526 |         -18.55 |        3:20:00 |     2     0     4  33.3 |
|      ENJ/USDT:USDT |        29 |          -3.97 |        -115.17 |          -229.963 |         -23.00 |        1:10:00 |    16     0    13  55.2 |
|              TOTAL |     24973 |           1.91 |       47641.96 |         95130.589 |        9513.06 |        2:54:00 | 19177     0  5796  76.8 |
=========================================================== LEFT OPEN TRADES REPORT ===========================================================
|          Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|---------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| HOT/USDT:USDT |         1 |          -5.81 |          -5.81 |           -11.615 |          -1.16 |        6:00:00 |     0     0     1     0 |
| XTZ/USDT:USDT |         1 |          -9.43 |          -9.43 |           -18.853 |          -1.89 |        8:00:00 |     0     0     1     0 |
| OMG/USDT:USDT |         1 |         -11.88 |         -11.88 |           -23.759 |          -2.38 |        6:00:00 |     0     0     1     0 |
| TLM/USDT:USDT |         1 |         -16.02 |         -16.02 |           -32.035 |          -3.20 |        7:00:00 |     0     0     1     0 |
|         TOTAL |         4 |         -10.78 |         -43.14 |           -86.260 |          -8.63 |        6:45:00 |     0     0     4     0 |
=========================================================== ENTER TAG STATS ===========================================================
|   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |     24973 |           1.91 |       47641.96 |         95130.589 |        9513.06 |        2:54:00 | 19177     0  5796  76.8 |
======================================================= EXIT REASON STATS ========================================================
|        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
| trailing_stop_loss |   20349 |  16596     0  3753  81.6 |           3.26 |       66375.1  |        132580     |       16593.8  |
|                roi |    2621 |   2581     0    40  98.5 |          16.51 |       43284.1  |         86418.6   |       10821    |
|          stop_loss |    1877 |      0     0  1877     0 |         -31.81 |      -59705.3  |       -119251     |      -14926.3  |
|         exit_short |     114 |      0     0   114     0 |         -18.33 |       -2089.19 |         -4173.18  |        -522.3  |
|          exit_long |       8 |      0     0     8     0 |         -22.44 |        -179.52 |          -358.372 |         -44.88 |
|         force_exit |       4 |      0     0     4     0 |         -10.78 |         -43.14 |           -86.26  |         -10.78 |
======================= MONTH BREAKDOWN ========================
|      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
|------------+-------------------+--------+---------+----------|
| 31/01/2021 |          5744.13  |    922 |       0 |      333 |
| 28/02/2021 |          5435.01  |    866 |       0 |      352 |
| 31/03/2021 |          1843.92  |    737 |       0 |      275 |
| 30/04/2021 |          6002.79  |    907 |       0 |      323 |
| 31/05/2021 |         11809.6   |   1087 |       0 |      336 |
| 30/06/2021 |          5371.51  |    793 |       0 |      241 |
| 31/07/2021 |          1098.27  |    587 |       0 |      206 |
| 31/08/2021 |          3862.53  |    764 |       0 |      271 |
| 30/09/2021 |          4325.52  |    742 |       0 |      213 |
| 31/10/2021 |          1428.59  |    565 |       0 |      181 |
| 30/11/2021 |          3672.24  |    687 |       0 |      202 |
| 31/12/2021 |          4036.71  |    673 |       0 |      187 |
| 31/01/2022 |          3067.24  |    607 |       0 |      172 |
| 28/02/2022 |          3214.18  |    588 |       0 |      171 |
| 31/03/2022 |           675.658 |    447 |       0 |      155 |
| 30/04/2022 |          4026.66  |    632 |       0 |      136 |
| 31/05/2022 |          4868.86  |    792 |       0 |      294 |
| 30/06/2022 |          3896.77  |    742 |       0 |      256 |
| 31/07/2022 |          1434.28  |    552 |       0 |      154 |
| 31/08/2022 |          1471.17  |    482 |       0 |      136 |
| 30/09/2022 |          1252.93  |    451 |       0 |      125 |
| 31/10/2022 |          1012.1   |    268 |       0 |       58 |
| 30/11/2022 |          2946.09  |    517 |       0 |      128 |
| 31/12/2022 |          1473.53  |    234 |       0 |       38 |
| 31/01/2023 |           282.98  |    414 |       0 |      148 |
| 28/02/2023 |          2203.52  |    475 |       0 |      122 |
| 31/03/2023 |          1126.7   |    497 |       0 |      133 |
| 30/04/2023 |           924.364 |    293 |       0 |       56 |
| 31/05/2023 |          1067.74  |    293 |       0 |       56 |
| 30/06/2023 |          1718.21  |    333 |       0 |       86 |
| 31/07/2023 |          1756.1   |    355 |       0 |       69 |
| 31/08/2023 |          1120.1   |    327 |       0 |       58 |
| 30/09/2023 |           457.045 |    258 |       0 |       58 |
| 31/10/2023 |           503.578 |    290 |       0 |       67 |
===================== SUMMARY METRICS =====================
| Metric                      | Value                     |
|-----------------------------+---------------------------|
| Backtesting from            | 2021-01-02 06:00:00       |
| Backtesting to              | 2023-10-27 00:00:00       |
| Max open trades             | 4                         |
|                             |                           |
| Total/Daily Avg Trades      | 24973 / 24.32             |
| Starting balance            | 1000 USDT                 |
| Final balance               | 96130.589 USDT            |
| Absolute profit             | 95130.589 USDT            |
| Total profit %              | 9513.06%                  |
| CAGR %                      | 406.66%                   |
| Sortino                     | 68.32                     |
| Sharpe                      | 74.80                     |
| Calmar                      | 1250.49                   |
| Profit factor               | 1.57                      |
| Expectancy (Ratio)          | 3.81 (0.13)               |
| Trades per day              | 24.32                     |
| Avg. daily profit %         | 9.26%                     |
| Avg. stake amount           | 199.763 USDT              |
| Total trade volume          | 4988672.2 USDT            |
|                             |                           |
| Long / Short                | 2191 / 22782              |
| Total profit Long %         | 1002.85%                  |
| Total profit Short %        | 8510.21%                  |
| Absolute profit Long        | 10028.524 USDT            |
| Absolute profit Short       | 85102.065 USDT            |
|                             |                           |
| Best Pair                   | OMG/USDT:USDT 4557.57%    |
| Worst Pair                  | ENJ/USDT:USDT -115.17%    |
| Best trade                  | HOT/USDT:USDT 20.13%      |
| Worst trade                 | 1000XEC/USDT:USDT -52.37% |
| Best day                    | 1179.226 USDT             |
| Worst day                   | -445.281 USDT             |
| Days win/draw/lose          | 698 / 9 / 322             |
| Avg. Duration Winners       | 2:25:00                   |
| Avg. Duration Loser         | 4:32:00                   |
| Max Consecutive Wins / Loss | 57 / 11                   |
| Rejected Entry signals      | 1045749                   |
| Entry/Exit Timeouts         | 0 / 11980                 |
|                             |                           |
| Min balance                 | 1019.604 USDT             |
| Max balance                 | 96216.849 USDT            |
| Max % of account underwater | 26.15%                    |
| Absolute Drawdown (Account) | 14.15%                    |
| Absolute Drawdown           | 963.229 USDT              |
| Drawdown high               | 5806.346 USDT             |
| Drawdown low                | 4843.117 USDT             |
| Drawdown Start              | 2021-02-01 00:00:00       |
| Drawdown End                | 2021-02-13 04:00:00       |
| Market change               | 37.70%                    |
===========================================================

Backtested 2021-01-02 06:00:00 -> 2023-10-27 00:00:00 | Max open trades : 4
================================================================================ STRATEGY SUMMARY ================================================================================
|                  Strategy |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |             Drawdown |
|---------------------------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------+----------------------|
| RSI_BB_MACD_Nov_2023_1h_2_Dec|     24973 |           1.91 |       47641.96 |         95130.589 |        9513.06 |        2:54:00 | 19177     0  5796  76.8 | 963.229 USDT  14.15% |
==================================================================================================================================================================================



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
    