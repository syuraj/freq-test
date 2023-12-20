#!/bin/bash

if [[ $(yq eval ".services.$1" ./docker/docker-compose-1.yml) != "null" ]]; then
    node='ubuntu@sunfreq.ddns.net'
    compose_yml_path="./docker/docker-compose-1.yml"
else
    node='ubuntu@sunfreq2.ddns.net'
    compose_yml_path="./docker/docker-compose-2.yml"
fi

rsync -rvth --progress --filter=':- .gitignore' ./ $node:~/freq-test --rsync-path="sudo rsync"

ssh -t $node "bash -lic \"cd ~/freq-test; d stop ${1}; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} up -d; d ps\""
