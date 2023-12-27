
# backtest first
# docker compose -f ./docker-compose-1.yml run  --rm hippo_SMAOffset hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102
timerange='20231001-20231210'
echo "backtesting for range $timerange"

# freqtrade backtesting --config ./user_data/configs_backtest/config_dev.json --strategy $1 --timerange $timerange --cache none --export signals 3>&1 1>&2 2>&3 | grep -v "INFO"
freqtrade backtesting --config ./user_data/configs_backtest/config_dev.json --strategy $1 --timerange $timerange --cache none --export signals
freqtrade backtesting-analysis --config ./user_data/configs_backtest/config_dev.json --analysis-to-csv --analysis-groups 0 1

# freqtrade backtesting --config ./user_data/configs_backtest/config_basic.json --timerange $timerange --strategy $strategy --cache none 3>&1 1>&2 2>&3 | grep -v "INFO"

# run hyperopt directly, but may choke your machine
# freqtrade hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss MaxDrawDownHyperOptLoss --spaces default --strategy $1 -e 10 --ignore-missing-spaces --timerange 20231201-20231210

# docker compose -f ./docker-compose-1.yml run  --rm hippo_SMAOffset hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102

# run hyperopt using docker but may be slower
# docker run --rm -it -v ./user_data:/freqtrade/user_data:rw --cpus=0.95 freqtradeorg/freqtrade:stable hyperopt --config /freqtrade/user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 10 --ignore-missing-spaces -i 1h --timerange 20231201-20231210
