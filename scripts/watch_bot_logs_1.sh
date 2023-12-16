#!/bin/bash

ssh -t ubuntu@sunfreq.ddns.net <<'EOF'
    while true; do
        for container_id in $(docker ps -q); do
            container_name=$(docker inspect --format '{{.Name}}' $container_id | cut -c2-)
            echo "Watching logs for container $container_name"
            last_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "-10 seconds")
            docker logs --tail 100 --since="$last_timestamp" $container_id 2>&1 | grep --line-buffered -Ei "error|warning|exception" | grep -v "uvicorn.error"
        done
        sleep 10
    done
EOF
