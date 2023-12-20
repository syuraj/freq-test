#!/bin/bash

if [ $(docker compose -f ./docker-compose-1.yml config --services | grep -m 1 $1) ]; then
    ssh -o ConnectTimeout=10 -t ubuntu@sunfreq.ddns.net "bash -lc \" sudo docker exec -it $1 /bin/bash \""
else
    ssh -o ConnectTimeout=10 -t ubuntu@sunfreq2.ddns.net "bash -lc \" sudo docker exec -it $1 /bin/bash \""
fi
