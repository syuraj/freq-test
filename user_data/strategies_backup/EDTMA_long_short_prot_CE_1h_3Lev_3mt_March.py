from datetime import datetime, timedelta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta
import pandas_ta as pta
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame, Series
from freqtrade.strategy import DecimalParameter, IntParameter, CategoricalParameter
from functools import reduce

# Chandalier Exit
'''
The "Chandelier Exit" technical indicator, also known as the "ATR Trailing Stop", is a volatility-based stop loss indicator that adjusts the stop loss level based on the average true range (ATR) of a cryptocurrency.

This code imports the necessary libraries (pandas and numpy) and defines a function called chandelier_exit() that takes a DataFrame of cryptocurrency data (with columns for "high", "low", and "close") and the ATR period and ATR multiplier as inputs. The function first calculates the ATR of the cryptocurrency and stores it in a new column called "atr". It then calculates the Chandelier Exit (ATR Trailing Stop) by subtracting the ATR multiplied by the ATR multiplier from the high price and stores it in a new column called "chandelier_exit".
'''
def chandelier_exit(df, atr_period=22, atr_mult=3):
    # Calculate the average true range (ATR)
    df['TR'] = df[['high', 'low', 'close']].apply(lambda x: max(x) - min(x), axis=1)
    df['atr'] = df['TR'].rolling(atr_period).mean()
    
    # Calculate the Chandelier Exit (ATR Trailing Stop)
    df['chandelier_exit_sl'] = df['high'] - df['atr'] * atr_mult
    df['chandelier_exit_tp'] = df['high'] + df['atr'] * atr_mult
    df['chandelier_exit_tp_short'] = df['low'] - df['atr'] * atr_mult
    df['chandelier_exit_sl_short'] = df['close'] + df['atr'] * atr_mult
    return df


# ############################################################################################################################################################################################


class EDTMA_Long_Short_prot_CE_1h_3Lev_3mt_March(IStrategy):
    

    minimal_roi = {
        "0": 0.238,
        "362": 0.148,
        "881": 0.066,
        "1039": 0
        
    }



    '''

    (((hit)))
            docker-compose run --rm freqtrade backtesting --strategy EDTMA_Long_Short_prot_CE_1h_3Lev_3mt_March -i 1h --export trades --breakdown month --timerange 20211101-20221208

            =========================================================== ENTER TAG STATS ===========================================================
            |   TAG |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
            |-------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
            | TOTAL |      6402 |           0.75 |        4801.07 |          7176.276 |         717.63 |        2:32:00 |  4623    13  1766  72.2 |
            ======================================================= EXIT REASON STATS ========================================================
            |        Exit Reason |   Exits |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
            |--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
            | trailing_stop_loss |    4982 |   4424     0   558  88.8 |           2.86 |       14264.8  |         21324.5   |        4754.94 |
            |          stop_loss |     826 |      0     0   826     0 |         -12.14 |      -10024    |        -14988.2   |       -3341.32 |
            |         ce_sl_long |     381 |     43     0   338  11.3 |          -4    |       -1523.74 |         -2279.32  |        -507.91 |
            |                roi |     210 |    156    13    41  74.3 |           9.96 |        2092.57 |          3132.24  |         697.52 |
            |         force_exit |       3 |      0     0     3     0 |          -2.88 |          -8.63 |           -12.949 |          -2.88 |
            ========================================================= LEFT OPEN TRADES REPORT =========================================================
            |      Pair |   Entries |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
            |-----------+-----------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
            |  XLM/USDT |         1 |          -2.11 |          -2.11 |            -3.171 |          -0.32 |       16:00:00 |     0     0     1     0 |
            |  BAT/USDT |         1 |          -2.53 |          -2.53 |            -3.796 |          -0.38 |       16:00:00 |     0     0     1     0 |
            | KAVA/USDT |         1 |          -3.99 |          -3.99 |            -5.983 |          -0.60 |        5:00:00 |     0     0     1     0 |
            |     TOTAL |         3 |          -2.88 |          -8.63 |           -12.949 |          -1.29 |       12:20:00 |     0     0     3     0 |
            ======================= MONTH BREAKDOWN ========================
            |      Month |   Tot Profit USDT |   Wins |   Draws |   Losses |
            |------------+-------------------+--------+---------+----------|
            | 30/11/2021 |           249.03  |    320 |      11 |      131 |
            | 31/12/2021 |           846.226 |    433 |       2 |      146 |
            | 31/01/2022 |           822.756 |    407 |       0 |      137 |
            | 28/02/2022 |           611.605 |    351 |       0 |      110 |
            | 31/03/2022 |           363.785 |    328 |       0 |      139 |
            | 30/04/2022 |           698.177 |    329 |       0 |       93 |
            | 31/05/2022 |           618.904 |    435 |       0 |      194 |
            | 30/06/2022 |           569.778 |    460 |       0 |      190 |
            | 31/07/2022 |           552.419 |    378 |       0 |      156 |
            | 31/08/2022 |           641.539 |    326 |       0 |      121 |
            | 30/09/2022 |           -41.287 |    266 |       0 |      129 |
            | 31/10/2022 |           277.9   |    197 |       0 |       79 |
            | 30/11/2022 |           844.638 |    327 |       0 |      120 |
            | 31/12/2022 |           120.806 |     66 |       0 |       21 |
            ================== SUMMARY METRICS ===================
            | Metric                      | Value                |
            |-----------------------------+----------------------|
            | Backtesting from            | 2021-11-01 00:00:00  |
            | Backtesting to              | 2022-12-08 00:00:00  |
            | Max open trades             | 3                    |
            |                             |                      |
            | Total/Daily Avg Trades      | 6402 / 15.93         |
            | Starting balance            | 1000 USDT            |
            | Final balance               | 8176.276 USDT        |
            | Absolute profit             | 7176.276 USDT        |
            | Total profit %              | 717.63%              |
            | CAGR %                      | 573.85%              |
            | Profit factor               | 1.37                 |
            | Trades per day              | 15.93                |
            | Avg. daily profit %         | 1.79%                |
            | Avg. stake amount           | 149.531 USDT         |
            | Total trade volume          | 957298.237 USDT      |
            |                             |                      |
            | Long / Short                | 2192 / 4210          |
            | Total profit Long %         | 242.85%              |
            | Total profit Short %        | 474.78%              |
            | Absolute profit Long        | 2428.492 USDT        |
            | Absolute profit Short       | 4747.785 USDT        |
            |                             |                      |
            | Best Pair                   | XRP/USDT 402.40%     |
            | Worst Pair                  | GRT/USDT -62.43%     |
            | Best trade                  | SNX/USDT 24.32%      |
            | Worst trade                 | 1000XEC/USDT -18.49% |
            | Best day                    | 295.063 USDT         |
            | Worst day                   | -120.02 USDT         |
            | Days win/draw/lose          | 249 / 4 / 147        |
            | Avg. Duration Winners       | 1:53:00              |
            | Avg. Duration Loser         | 4:04:00              |
            | Rejected Entry signals      | 665093               |
            | Entry/Exit Timeouts         | 0 / 1959             |
            |                             |                      |
            | Min balance                 | 1001.7 USDT          |
            | Max balance                 | 8248.829 USDT        |
            | Max % of account underwater | 20.55%               |
            | Absolute Drawdown (Account) | 8.73%                |
            | Absolute Drawdown           | 465.462 USDT         |
            | Drawdown high               | 4333.078 USDT        |
            | Drawdown low                | 3867.616 USDT        |
            | Drawdown Start              | 2022-05-12 05:00:00  |
            | Drawdown End                | 2022-05-23 19:00:00  |
            | Market change               | -79.30%              |
            ======================================================
    
    
    '''
    

    # Optimal timeframe for the strategy
    timeframe = '1h'

    # Can this strategy go short?
    can_short: bool = True

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    startup_candle_count = 30

    

    # Disabled
    stoploss = -0.12

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True


    #leverage here
    leverage_optimize = False
    leverage_num = IntParameter(low=1, high=4, default=3, space='buy', optimize=leverage_optimize)

    # Custom stoploss
    use_custom_stoploss = False
    is_optimize_32 = True

    s_buy_adx_enabled = CategoricalParameter([True, False], default=True)

    s_buy_adx = IntParameter(20, 75, default=26, space="buy", optimize=s_buy_adx_enabled)
    s_buy_dema = IntParameter(45, 65, default=53, space="buy")
    s_buy_ema = IntParameter(100, 210, default=102, space="buy")

    

    s_buy_tema = IntParameter(6, 20, default=19, space="buy")
    # s_sell_adx_enabled = CategoricalParameter([True, False], default=True)

    # s_sell_adx = IntParameter(20, 75, default=73, space="sell", optimize=s_sell_adx_enabled)
    # s_sell_dema = IntParameter(45, 65, default=46, space="sell")
    # s_sell_ema = IntParameter(100, 210, default=159, space="sell")
    # s_sell_tema = IntParameter(6, 20, default=10, space="sell")

    buy_adx_enabled = CategoricalParameter([True, False], default=True)


    buy_adx = IntParameter(20, 75, default=35, space="buy", optimize=buy_adx_enabled)
    buy_dema = IntParameter(45, 65, default=45, space="buy")
    buy_ema = IntParameter(100, 210, default=177, space="buy")

    

    buy_tema = IntParameter(6, 20, default=7, space="buy")

    # sell_adx_enabled = CategoricalParameter([True, False], default=True)

    # sell_adx = IntParameter(20, 75, default=35, space="sell", optimize=sell_adx_enabled)
    # sell_dema = IntParameter(45, 65, default=59, space="sell")
    # sell_ema = IntParameter(100, 210, default=128, space="sell")
    # sell_tema = IntParameter(6, 20, default=13, space="sell")


    
    ce_l_atr_period = IntParameter(5, 40, default=23, space="sell")
    ce_l_atr_mult = IntParameter(1, 6, default=1, space="sell")
    ce_s_atr_period = IntParameter(5, 40, default=26, space="sell")
    ce_s_atr_mult = IntParameter(1, 6, default=6, space="sell")

    # sell_fastx = IntParameter(50, 100, default=70, space='sell', optimize=False)

    protect_optimize = False
    # cooldown_lookback = IntParameter(1, 240, default=6, space="protection", optimize=protect_optimize)
    max_drawdown_lookback = IntParameter(1, 288, default=10, space="protection", optimize=protect_optimize)
    max_drawdown_trade_limit = IntParameter(1, 20, default=1, space="protection", optimize=protect_optimize)
    max_drawdown_stop_duration = IntParameter(1, 288, default=6, space="protection", optimize=protect_optimize)
    max_allowed_drawdown = DecimalParameter(0.10, 0.50, default=0.12, decimals=2, space="protection",
                                            optimize=protect_optimize)
    stoploss_guard_lookback = IntParameter(1, 288, default=3, space="protection", optimize=protect_optimize)
    stoploss_guard_trade_limit = IntParameter(1, 20, default=1, space="protection", optimize=protect_optimize)
    stoploss_guard_stop_duration = IntParameter(1, 288, default=6, space="protection", optimize=protect_optimize)

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

    

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        
        dataframe['volume_mean_20'] = dataframe['volume'].rolling(22).mean().shift(1)


        

        # ADX
        dataframe['adx'] = ta.ADX(dataframe)

        

        # TEMA - Triple Exponential Moving Average
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=self.s_buy_tema.value)
        dataframe['dema'] = ta.DEMA(dataframe, timeperiod=self.s_buy_dema.value)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=self.s_buy_ema.value)

        # dataframe['tema_s'] = ta.TEMA(dataframe, timeperiod=self.s_sell_tema.value)
        # dataframe['dema_s'] = ta.DEMA(dataframe, timeperiod=self.s_sell_dema.value)
        # dataframe['ema200_s'] = ta.EMA(dataframe, timeperiod=self.s_sell_ema.value)


        dataframe['l_tema'] = ta.TEMA(dataframe, timeperiod=self.buy_tema.value)
        dataframe['l_dema'] = ta.DEMA(dataframe, timeperiod=self.buy_dema.value)
        dataframe['l_ema200'] = ta.EMA(dataframe, timeperiod=self.buy_ema.value)

        # dataframe['l_tema_s'] = ta.TEMA(dataframe, timeperiod=self.sell_tema.value)
        # dataframe['l_dema_s'] = ta.DEMA(dataframe, timeperiod=self.sell_dema.value)
        # dataframe['l_ema200_s'] = ta.EMA(dataframe, timeperiod=self.sell_ema.value)



        long_chandelier_exit = chandelier_exit(df=dataframe, atr_period = self.ce_l_atr_period.value, atr_mult = self.ce_l_atr_mult.value)

        dataframe['ce_atr'] = long_chandelier_exit['atr']
        dataframe['ce_chandelier_exit_sl'] = long_chandelier_exit['chandelier_exit_sl']
        dataframe['ce_chandelier_exit_tp'] = long_chandelier_exit['chandelier_exit_tp']

        short_chandelier_exit = chandelier_exit(df=dataframe, atr_period = self.ce_s_atr_period.value, atr_mult = self.ce_s_atr_mult.value)

        dataframe['ce_chandelier_exit_tp_short'] = short_chandelier_exit['chandelier_exit_tp_short']
        dataframe['ce_chandelier_exit_sl_short'] = short_chandelier_exit['chandelier_exit_sl_short']



        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        
        dataframe.loc[(
                (dataframe['adx'] > self.buy_adx.value) &
                (dataframe['l_tema'] > dataframe['l_dema']) &  # Guard: tema is raising
                (dataframe['l_dema'] > dataframe['l_ema200']) &  # Guard: tema is raising
                (dataframe['volume'] > dataframe['volume_mean_20'])
            ),  'enter_long'] = 1

        # if conditions_short:
        dataframe.loc[(
                (dataframe['adx'] > self.s_buy_adx.value) &
                (dataframe['tema'] < dataframe['dema']) &  # Guard: tema is raising
                (dataframe['dema'] < dataframe['ema200']) &  # Guard: tema is raising
                (dataframe['volume'] > dataframe['volume_mean_20'])
            ),  'enter_short'] = 1

        

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
                
        conditions_long = []
        conditions_short = []
        dataframe.loc[:, 'exit_tag'] = ''

        sell_1 = (
                (dataframe['low'] <= dataframe['ce_chandelier_exit_tp_short']) &
                (dataframe['volume'] > 0)
        )

        sell_2 = (
                (dataframe['high'] >= dataframe['ce_chandelier_exit_sl_short']) &
                
                (dataframe['volume'] > 0)
        )

        sell_3 = (
                (dataframe['high'] >= dataframe['ce_chandelier_exit_tp']) &
                
                (dataframe['volume'] > 0)
        )

        sell_4 = (
                (dataframe['low'] <= dataframe['ce_chandelier_exit_sl']) &

                (dataframe['volume'] > 0)
        )

        conditions_long.append(sell_3)
        dataframe.loc[sell_3, 'exit_tag'] += 'ce_tp_long'

        conditions_long.append(sell_4)
        dataframe.loc[sell_4, 'exit_tag'] += 'ce_sl_long'

        conditions_short.append(sell_1)
        dataframe.loc[sell_1, 'exit_tag'] += 'ce_tp_short'

        conditions_short.append(sell_2)
        dataframe.loc[sell_2, 'exit_tag'] += 'ce_sl_short'

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