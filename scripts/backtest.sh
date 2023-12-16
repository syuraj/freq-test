#!/bin/bash

# strategies_folder='./user_data/strategies'
# # strategies=("$strategies_folder"/*)
# strategies=("${strategies_folder[@]##*/}")

# echo "${strategies}"

strategies_folder='./user_data/strategies/'
stratigies=$(find "$strategies_folder" -maxdepth 1 -type f -name "*.py" ! -name "__init__.py" -exec basename {} \; | sed 's/\.[^.]*$//')

freqtrade backtesting --config ./user_data/configs_backtest/config_basic.json --timerange 20230101-20231201 --strategy-list $stratigies
