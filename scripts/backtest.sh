#!/bin/bash

# strategies_folder='./user_data/strategies'
# # strategies=("$strategies_folder"/*)
# strategies=("${strategies_folder[@]##*/}")

# echo "${strategies}"

strategies_folder='./user_data/strategies/'
stratigies=$(find "$strategies_folder" -maxdepth 1 -type f -name "*.py" -exec basename {} \; | sed 's/\.[^.]*$//')

freqtrade backtesting --strategy-list $stratigies --config ./user_data/configs_backtest/config.json --timerange 20191230-20230930
