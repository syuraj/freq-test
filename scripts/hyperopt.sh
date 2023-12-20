
# freqtrade hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss MaxDrawDownHyperOptLoss --spaces default --strategy $1 -e 10 --ignore-missing-spaces -i 1h --timerange 20231201-20231202

# docker compose -f ./docker-compose-1.yml run  --rm hippo_SMAOffset hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102

docker run --rm -it -v ./user_data:/freqtrade/user_data:rw --cpus=0.9 freqtradeorg/freqtrade:stable hyperopt --config /freqtrade/user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208
