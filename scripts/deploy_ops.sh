#!/bin/bash

rsync -rvth --progress --filter=':- .gitignore' ./ ubuntu@sunfreq2.ddns.net:~/freq-test --rsync-path="sudo rsync"
compose_yml_path='./docker/docker-compose-ops.yml'

if [ "$1" == "--restart" ]; then
    echo "Stopping and deploying new containers"
    ssh ubuntu@sunfreq2.ddns.net "bash -lic 'cd ~/freq-test; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} down; d compose -f ${compose_yml_path} up -d; d ps'"
else
    echo "Deploying containers only if yml change"
    ssh ubuntu@sunfreq2.ddns.net "bash -lic 'cd ~/freq-test; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} up -d; d ps'"
fi