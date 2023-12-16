#!/bin/bash

strategies_folder='./user_data/strategies/'
stratigies=$(find "$strategies_folder" -maxdepth 1 -type f -name "*.py" ! -name "__init__.py" -exec basename {} \; | sed 's/\.[^.]*$//')
strategies_str=$(IFS=","; echo "${stratigies[*]}")
echo "Running backtest on these strategies: "
echo $strategies_str

timerange="20230101-20231201"

for strategy in $stratigies; do
    echo "Starting backtest on $strategy ...."
    freqtrade backtesting --config ./user_data/configs_backtest/config_basic.json --timerange $timerange --strategy $strategy --cache none 3>&1 1>&2 2>&3 # | grep -v "INFO"
done
