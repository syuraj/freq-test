#!/bin/bash

nodes=('ubuntu@freq1.siristechnology.com' 'ubuntu@freq2.siristechnology.com')

deploy_to_node() {
    local node=$1
    local node_number=$2
    local custom_path=$3
    local restart_flag=$4

    if [ "$3" = 'ops' ]; then
        local compose_yml_path="./docker/docker-compose-ops-${node_number}.yml"
    else
        local compose_yml_path="./docker/docker-compose-${node_number}.yml"
    fi

    printf "\n deploying to $1 ....\n\n"

    rsync -rvth --progress --filter=':- .gitignore' ./ $node:~/freq-test --rsync-path="sudo rsync"

    if [ "$4" == "--restart" ]; then
        echo "Stopping and deploying new containers"
        ssh -t $node "bash -lic \"cd ~/freq-test; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} down; d compose -f ${compose_yml_path} up -d; d ps\""
    else
        echo "Deploying containers only if yml change"
        ssh -t $node "bash -lic \"cd ~/freq-test; d compose -f ${compose_yml_path} build; d compose -f ${compose_yml_path} up -d; d ps\""
    fi
}

print_usage() {
    echo "Usage:"
    echo "  $(basename "$0")                        # Deploy without restart"
    echo "  $(basename "$0") --restart              # Deploy with stop and start"
    echo "  $(basename "$0") ops                    # Deploy ops without restart"
    echo "  $(basename "$0") ops --restart          # Deploy ops with stop and start"
}

if [ "$#" -eq 1 ] && [ "$1" == "--help" ]; then
    print_usage
    exit 0
fi

for ((i=0; i<${#nodes[@]}; i++)); do
    deploy_to_node "${nodes[$i]}" "$((i+1))" $1 "${!#}"
done
