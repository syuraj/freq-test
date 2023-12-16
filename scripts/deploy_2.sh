#!/bin/bash

rsync -rvth --progress --filter=':- .gitignore' ./ ubuntu@sunfreq2.ddns.net:~/freq-test --rsync-path="sudo rsync"

if [ "$1" == "--restart" ]; then
    echo "Stopping and deploying new containers"
    ssh ubuntu@sunfreq2.ddns.net "bash -lic 'cd ~/freq-test; d compose -f ./docker-compose-2.yml build; d compose -f ./docker-compose-2.yml down; d compose -f ./docker-compose-2.yml up -d; d ps'"
else
    echo "Deploying containers only if yml change"
    ssh ubuntu@sunfreq2.ddns.net "bash -lic 'cd ~/freq-test; d compose -f ./docker-compose-2.yml build; d compose -f ./docker-compose-2.yml up -d; d ps'"
fi