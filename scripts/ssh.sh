#!/bin/bash

if [ $(docker compose -f ./docker-compose-1.yml config --services | grep -m 1 $1) ]; then
    ssh -o ConnectTimeout=10 -t ubuntu@freq1.siristechnology.com "bash -lc \" sudo docker exec -it $1 /bin/bash \""
else
    ssh -o ConnectTimeout=10 -t ubuntu@freq2.siristechnology.com "bash -lc \" sudo docker exec -it $1 /bin/bash \""
fi
