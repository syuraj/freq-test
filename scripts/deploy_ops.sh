#!/bin/bash

if [ "$#" -eq 0 ]; then
  echo "Usage: ./scripts/deploy_ops.sh 1 --restart"
  exit 1
fi

node=''
if [ "$1" == "1" ]; then
    node='ubuntu@sunfreq.ddns.net'
else
    node='ubuntu@sunfreq2.ddns.net'
fi

rsync -rvth --progress --filter=':- .gitignore' ./ $node:~/freq-test --rsync-path="sudo rsync"
compose_yml_path="./docker/docker-compose-ops-${1}.yml"

if [ "$2" == "--restart" ]; then
    echo "Stopping and deploying new containers"
    ssh $node "bash -lic 'cd ~/freq-test; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} down; d compose -f ${compose_yml_path} up -d; d ps'"
else
    echo "Deploying containers only if yml change"
    ssh $node "bash -lic 'cd ~/freq-test; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} up -d; d ps'"
fi