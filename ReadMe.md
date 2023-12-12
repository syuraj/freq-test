## Setup Instructions
```mkdir ft_userdata```

```cd ft_userdata/```

#### Download the docker-compose file from the repository
```curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml```

#### Pull the freqtrade image
```d compose pull```

#### Create user directory structure
```d compose run --rm freqtrade create-userdir --userdir user_data```

#### Create configuration - Requires answering interactive questions
```d compose run --rm freqtrade new-config --config user_data/config.json```


## To download data
* with docker ```d compose run --rm freqtrade download-data --pairs BTC/USDT --exchange kraken --days 100 -t 5m```
* without docker ```f download-data --exchange binace --config ./user_data/configs_backtest/config.json --days 1000 -t 1h```

## To download list of crypto pairs
* with docker ```d compose run --rm freqtrade test-pairlist```
* without docker ```f test-pairlist```

## To backtest
* with docker ```d compose run --rm freqtrade backtesting --config user_data/config.json --strategy-list NostalgiaForInfinityV7 TwoMovingAveragesStrategy --timerange 20191230-20230930 -i 5m```
* without docker ```f backtesting --config user_data/configs/config.json --strategy-list NostalgiaForInfinityV7 TwoMovingAveragesStrategy --timerange 20191230-20230930 -i 5m```
* ```f backtesting --config user_data/backtest_configs/picasso_rsi_bb_binance.json --strategy-list RSI_BB_MACD_Nov_2023_1h_2_Dec --timerange 20191230-20230930 -i 1h```
* ```f backtesting --strategy-list TSPredict --config ./user_data/configs_backtest/config.json --timerange 20191230-20230930 -i 5m ```
* ```f backtesting --strategy-list EDTMA_Long_Short_prot_CE_1h_3Lev_3mt_Dec21_np_April CE_CTI_STC_EMA_1h_V5_3x_3mt_Jan16 CE_CTI_STC_EMA_1h_V5_4x_3mt_Jan16_np_Jan20 --config ./user_data/backtest_configs/picasso_EDTMA.json --timerange 20191230-20230930 -i 1h```

## To build new docker with dependencies
```d compose build --pull```

## To plot with docker
* with docker ```d compose run --rm freqtrade plot-dataframe --strategy NostalgiaForInfinityV7 -p BTC/USDT --timerange=20231201-20231207```
* without docker ```f plot-dataframe --strategy NostalgiaForInfinityV7 -p ETH/USDT --timerange=20191201-20231207```

## To run Jupiter
* ```d compose -f docker/docker-compose-jupyter.yml up```
* ```d compose -f docker/docker-compose-jupyter.yml build --no-cache```

## To keep running a strategy
```d compose run freqtrade trade --strategy NostalgiaForInfinityV7```

## To keep docker up & running
```d compose up -d```

## To convert data into freqtrade files
```freqtrade convert-trade-data --exchange kraken --format-from kraken_csv --format-to feather```
#### Convert trade data to different ohlcv timeframes
```freqtrade trades-to-ohlcv -p ETH/USDT ETH/USD ETC/USD --exchange kraken -t 1m 5m 15m 1h```
#### To list downloaded data
```d compose run freqtrade list-data -p ETH/USDT```

## To run grafana docker
* To create a persistent storage: ```d volume create grafana-storage```
* To run docker: ```d run -d -p 3000:3000 --name=grafana -v grafana-storage:/var/lib/grafana -v $(pwd)/user_data:/user_data grafana/grafana```

## To hpyeroptimize
* ```f hyperopt --config user_data/config-static-tutorial.json --hyperopt-loss SharpeHyperOptLoss --spaces buy sell --strategy SMAOffsetProtectOptV1 --epochs 10 --timerange=20230605- --disable-param-export```
