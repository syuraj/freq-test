
rsync -rvth --progress --filter=':- .gitignore' ./ ubuntu@141.145.212.19:~/freq-test --rsync-path="sudo rsync"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose build; d compose up -d; d ps -q | xargs -I {} sudo docker logs -f {}; wait'"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose build; d compose down; d compose up -d; d ps'"
ssh ubuntu@sunfreq.ddns.net "bash -lic 'cd ~/freq-test; d compose build; d compose up -d; d ps'"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'd ps -q | xargs -I {} sh -c 'echo "Watching logs for container: $(sudo docker inspect --format "{{.Name}}" {})"; sudo docker logs -f {} &' && wait'"

# ssh ubuntu@sunfreq.ddns.net "bash -lic 'docker ps -q | xargs -I {} sh -c '\''echo "Watching logs for container: $(docker inspect --format "{{.Name}}" {})"; docker logs -f {} &'\'' && wait'"
# ssh -t ubuntu@sunfreq.ddns.net 'bash -lic '\''docker ps -q | xargs -I {} sh -c '\''echo "Watching logs for container: $(docker inspect --format "{{.Name}}" {})"; docker logs -f {} &'\'' && wait'\'''


# ssh <username>@<remote_server> 'docker ps -q | xargs -I {} sh -c '\''echo "Watching logs for container: $(docker inspect --format "{{.Name}}" {})"; docker logs -f {} &'\'' && wait'
