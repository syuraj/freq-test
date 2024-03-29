#!/bin/bash

if [[ "$#" != 1 ]] ; then
    echo "Strategy name required. or use deploy-all.sh"
    exit 1
fi

if [[ $(yq eval ".services.$1" ./docker/docker-compose-1.yml) != "null" ]]; then
    node='ubuntu@freq1.siristechnology.com'
    compose_yml_path="./docker/docker-compose-1.yml"
else
    node='ubuntu@freq2.siristechnology.com'
    compose_yml_path="./docker/docker-compose-2.yml"
fi

rsync -rvth --progress --filter=':- .gitignore' ./ $node:~/freq-test --rsync-path="sudo rsync"

ssh -t $node "bash -lic \"cd ~/freq-test; d stop ${1}; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} up -d; d ps\""
