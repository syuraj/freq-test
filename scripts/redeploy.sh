#!/bin/bash

if [ $(docker compose -f ./docker-compose-1.yml config --services | grep -m 1 $1) ]; then
    ssh -o ConnectTimeout=10 ubuntu@sunfreq.ddns.net "bash -lc \"sudo docker stop $1 \"" && source ./scripts/deploy_1.sh
else
    ssh -o ConnectTimeout=10 ubuntu@sunfreq2.ddns.net "bash -lc \"sudo docker stop $1 \"" && source ./scripts/deploy_2.sh
fi
