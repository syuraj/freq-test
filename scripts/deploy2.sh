
rsync -rvth --progress --filter=':- .gitignore' ./ ubuntu@89.168.37.131:~/freq-test --rsync-path="sudo rsync"

ssh ubuntu@89.168.37.131 "bash -lic 'cd ~/freq-test; d compose -f ./docker-compose-2.yml build; d compose -f ./docker-compose-2.yml up -d; d ps'"
