
### Setup Instructions
mkdir ft_userdata
cd ft_userdata/
# Download the docker-compose file from the repository
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# Pull the freqtrade image
docker compose pull

# Create user directory structure
docker compose run --rm freqtrade create-userdir --userdir user_data

# Create configuration - Requires answering interactive questions
docker compose run --rm freqtrade new-config --config user_data/config.json


### To download data
`docker compose run --rm freqtrade download-data --pairs BTC/USDT --exchange kraken --days 5 -t 1h`

`freqtrade download-data --exchange kraken`
or using docker
`docker exec -it 6f840b9e644a freqtrade download-data --exchange kraken --pairs BTC/USDT ETH/USDT `

### To backtest

`docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --timerange 20190801-20191001 -i 5m`

