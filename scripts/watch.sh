#!/bin/bash

if [ "$#" -eq 0 ]; then
    while true; do
        printf "watching containers in node1 ....\n\n"
        ssh -o ConnectTimeout=10 ubuntu@freq1.siristechnology.com "sudo docker ps"
        printf "\nwatching containers in node2 ....\n\n"
        ssh -o ConnectTimeout=10 ubuntu@freq2.siristechnology.com "sudo docker ps"
        sleep 15
        clear
    done
fi

if [ $(docker compose -f ./docker/docker-compose-1.yml config --services | grep -m 1 $1) ]; then
    ssh -o ConnectTimeout=10 ubuntu@freq1.siristechnology.com "bash -lc \" sudo docker logs --tail 100 -f $1 && sleep infinity \""
else
    ssh -o ConnectTimeout=10 ubuntu@freq2.siristechnology.com "bash -lc \" sudo docker logs --tail 100 -f $1 && sleep infinity \""
fi
