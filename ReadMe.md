## Setup Instructions
```mkdir ft_userdata```

```cd ft_userdata/```

#### Download the docker-compose file from the repository
```curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml```

#### Pull the freqtrade image
```docker compose pull```

#### Create user directory structure
```d compose run --rm freqtrade create-userdir --userdir user_data```

#### Create configuration - Requires answering interactive questions
```d compose run --rm freqtrade new-config --config user_data/config.json```


## To download data
* with docker ```d compose run --rm freqtrade download-data --pairs BTC/USDT --exchange kraken --days 100 -t 5m```
* without docker ```freqtrade download-data --exchange kraken```


## To download list of crypto pairs
```d compose run --rm freqtrade test-pairlist```

## To backtest
```d compose run --rm freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --timerange 20231201-20231207 -i 5m```

## To build new docker with dependencies
```d compose build --pull```

## To plot with docker
```d compose run --rm freqtrade plot-dataframe --strategy SampleStrategy -p BTC/USDT --timerange=20231201-20231207```

## To run Jupiter
* ```d compose -f docker/docker-compose-jupyter.yml up```
* ```d compose -f docker/docker-compose-jupyter.yml build --no-cache```

## To keep running a strategy
```d compose run freqtrade trade --strategy SampleStrategy```

## To keep docker up & running
```d compose up -d```
