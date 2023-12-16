
rsync -rvth --progress --filter=':- .gitignore' ./ ubuntu@141.145.212.19:~/freq-test --rsync-path="sudo rsync"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose build; d compose up -d; d ps -q | xargs -I {} sudo docker logs -f {}; wait'"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose build; d compose down; d compose up -d; d ps'"

if [ "$1" == "--restart" ]; then
    echo "Stopping and deploying new containers"
    ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose -f ./docker-compose-1.yml build; d compose -f ./docker-compose-1.yml down; d compose -f ./docker-compose-1.yml up -d; d ps'"
else
    echo "Deploying containers only if yml change"
    ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose -f ./docker-compose-1.yml build; d compose -f ./docker-compose-1.yml up -d; d ps'"
fi
# ssh ubuntu@sunfreq.ddns.net "bash -lic 'd ps -q | xargs -I {} sh -c 'echo "Watching logs for container: $(sudo docker inspect --format "{{.Name}}" {})"; sudo docker logs -f {} &' && wait'"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'docker ps -q | xargs -I {} sh -c '\''echo "Watching logs for container: $(docker inspect --format "{{.Name}}" {})"; docker logs -f {} &'\'' && wait'"
# ssh -t ubuntu@sunfreq.ddns.net 'bash -lic '\''docker ps -q | xargs -I {} sh -c '\''echo "Watching logs for container: $(docker inspect --format "{{.Name}}" {})"; docker logs -f {} &'\'' && wait'\'''


# ssh <username>@<remote_server> 'docker ps -q | xargs -I {} sh -c '\''echo "Watching logs for container: $(docker inspect --format "{{.Name}}" {})"; docker logs -f {} &'\'' && wait'
