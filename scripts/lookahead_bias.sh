#!/bin/bash

# strategies_folder='./user_data/strategies'
# # strategies=("$strategies_folder"/*)
# strategies=("${strategies_folder[@]##*/}")

# echo "${strategies}"

strategies_folder='./user_data/strategies/'
stratigies=$(find "$strategies_folder" -maxdepth 1 -type f -name "*.py" ! -name "__init__.py" -exec basename {} \; | sed 's/\.[^.]*$//')

freqtrade lookahead-analysis --strategy-list $stratigies --config ./user_data/configs_backtest/config.json --timerange 20230101-20231201
