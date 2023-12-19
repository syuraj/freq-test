

# freqtrade hyperopt --config ./user_data/configs_backtest/config_basic.json --hyperopt-loss MaxDrawDownHyperOptLoss --timerange 20231001-20231201 -e 100 --spaces all --strategy $1


# freqtrade hyperopt --config ./user_data/configs_backtest/config_basic.json --hyperopt-loss SharpeHyperOptLoss --timerange 20231001-20231201 -e 100 --spaces roi --strategy $1

# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy slope_is_dope_adx_1h_2Lev_dec14_3mt -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102

freqtrade hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102

# d compose run --rm freqtrade hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102

# docker compose -f ./docker-compose-1.yml run  --rm hippo_SMAOffset hyperopt --config ./user_data/configs_backtest/config_dev.json --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy $1 -e 155 --ignore-missing-spaces -i 1h --timerange 20220101-20221208 --random-state 10102
