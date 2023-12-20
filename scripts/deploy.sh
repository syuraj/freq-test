#!/bin/bash

if [[ $(yq eval ".services.$1" ./docker/docker-compose-1.yml) != "null" ]]; then
    ssh -o ConnectTimeout=10 ubuntu@sunfreq.ddns.net "bash -lc \"sudo docker stop $1 \"" && source ./scripts/deploy-all.sh
else
    ssh -o ConnectTimeout=10 ubuntu@sunfreq2.ddns.net "bash -lc \"sudo docker stop $1 \"" && source ./scripts/deploy-all.sh
fi
