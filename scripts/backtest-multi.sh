#!/bin/bash

CONFIG_FILE='./user_data/configs_backtest/config_basic.json'

STRATEGY_NAME='TwoMovingAveragesStrategy'

PARAMETER_SETS=(
    "rsi-length=14 ema-fast=10 ema-slow=30"
    "rsi-length=20 ema-fast=15 ema-slow=35"
    "rsi-length=25 ema-fast=20 ema-slow=40"
)

LOG_DIR="parameter_test_logs_2ma"
RESULTS_DIR="backtesting_results_2ma"
mkdir -p "$LOG_DIR" "$RESULTS_DIR"

for PARAMETER_SET in "${PARAMETER_SETS[@]}"; do
    # Create a unique identifier for each run
    RUN_ID=$(echo "$PARAMETER_SET" | tr ' ' '_')

    # Run Freqtrade backtesting with the specified parameter set and export results to CSV
    freqtrade backtesting --config "$CONFIG_FILE" --strategy "$STRATEGY_NAME" --datadir "data/${RUN_ID}" --timerange 20211201-20221201 --export trades --export-filename "$RESULTS_DIR/backtest_results_${RUN_ID}.csv"

    # Save the log file
    LOG_FILE="${LOG_DIR}/log_${RUN_ID}_backtesting.txt"
    cp freqtrade-user.log "$LOG_FILE"

    # Optional: You may want to parse and extract relevant information from the log file for analysis.
done
