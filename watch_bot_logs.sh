#!/bin/bash

ssh -t ubuntu@sunfreq.ddns.net 'bash -c "docker ps -q | xargs -I {} sh -c '\''echo Watching logs for container: {}; docker logs -f {} &'\''" && sleep 60'
