#!/bin/bash

ssh -t ubuntu@sunfreq2.ddns.net <<'EOF'
    d='sudo docker'
    while true; do
        for container_id in $($d ps -q); do
            container_name=$($d inspect --format '{{.Name}}' $container_id | cut -c2-)
            echo "Watching logs for container $container_name"
            last_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "-10 seconds")
            $d logs --tail 100 --since="$last_timestamp" $container_id 2>&1 | grep --line-buffered -Ei "error|warning|exception" | grep -v "uvicorn.error"
        done
        sleep 10
    done
EOF
