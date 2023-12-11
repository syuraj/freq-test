
rsync -rvth --progress --filter=':- .gitignore' ./ ubuntu@141.145.212.19:~/freq-test --rsync-path="sudo rsync"

ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose build; d compose up -d'"
