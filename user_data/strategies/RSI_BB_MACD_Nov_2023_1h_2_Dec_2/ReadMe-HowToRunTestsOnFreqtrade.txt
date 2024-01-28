Step - 1: Please install docker on to your system/laptop/pc

Step - 2: follow below given instructions on you command-prompt/powershell/bash (if anything mentioned here doesn't resonate, can check out freqtrade setup documentation given in this link -  https://www.freqtrade.io/en/0.18.1/installation/)

# Creating the project folder ############################################################################

mkdir ft_userdata

# Access to the directory ################################################################################

cd ft_userdata/

# Download docker compose from the repository ############################################################

curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# Obtaining the freqtrade image ##########################################################################

docker-compose pull

# Create subdirectory ####################################################################################

docker-compose run --rm freqtrade create-userdir --userdir user_data

# Launch the interactive bot configuration ###############################################################

docker-compose run --rm freqtrade new-config --config user_data/config.json


Step - 3: Replace user_data/strategies/sample_strategy.py with the `CE_CTI_STC_V3_Sharing_Jan12.py` (--Startegy name has to be replaced here--) file given in the zip

Step - 4: Replace user_data/config.json with .json file given in the zip.

Step - 5: You have to download the data for backtesting... 

docker-compose run --rm freqtrade download-data --timerange 20210101-20230616 -t 5m 15m 1h 4h 8h 1d

Step - 6: You can run backtesting of the strategy by mentioning strategy name as given below

docker-compose run --rm freqtrade backtesting --strategy CE_CTI_STC_EMA_1h_V3_4x_3mt_Dec29 (--Startegy name has to be replaced here--) -i 1h --export trades --breakdown month --timerange 20210101-20221208


Step - 7: to run live or dry run test, you need to edit docker-compose.yml file 

# change "ports" as mentioned below ###############################################################

ports:
  - "8080:8080"

# and also in "command" under "trade" , beside "--strategy", you have to mention strategy name given to make the bot run successfully. ###############################################################

command: >
 trade
 --strategy CE_CTI_STC_EMA_1h_V3_4x_3mt_Dec29 (--Startegy name has to be replaced here--)

Step - 8: to go live or run the bot with dry-run settings can type below command in command-promt

# docker-compose up (to start) and down (to end) ###############################################################
docker-compose up

Step - 9: You can mention your binance api key in config.json by enabling "futures" option in binance account of yours. Freqtrade accepts more than 70+ exchanges apart from binance, you can mention your respective exchange api key and secret in config.json . You can also connect to telegram for ease of access to bot performance by mentioning key and chat_id . steps are given in the link I mentioned in "Step - 2" for the same.

Please email me for any further assistance at any given time, "pichupicasso@gmail.com" and CC the same too "pradeeppicassop@gmail.com"

Thank You.
regards,
Puranam Pradeep Picasso
https://www.linkedin.com/in/puranampradeeppicasso/