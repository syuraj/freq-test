#!/bin/bash

# ssh -t ubuntu@sunfreq.ddns.net 'bash -c "docker ps -q | xargs -I {} sh -c '\''echo Watching logs for container: {}; docker logs -f {} &'\''" && sleep 60'
# ssh -t ubuntu@sunfreq.ddns.net 'bash -c "docker ps -q | xargs -I {} sh -c '\''echo Watching error logs for container: {}; docker logs -f {} 2>&1 | grep --line-buffered -i '\''error'\'' &'\''" && sleep 999999'

ssh -t ubuntu@sunfreq2.ddns.net <<'EOF'
sudo docker ps -q | xargs -I {} sh -c 'echo Watching logs for container: {}; sudo docker logs -f {} 2>&1 | grep --line-buffered -Ei "error|warning|exception" &' && sleep 999999
EOF

