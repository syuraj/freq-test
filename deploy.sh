
rsync -arvth --delete --progress --filter=':- .gitignore' ./ ubuntu@141.145.212.19:~/freq-test

ssh ubuntu@141.145.212.19 "bash -lc 'cd ~/freq-test; sudo docker compose build; sudo docker compose up -d'"
