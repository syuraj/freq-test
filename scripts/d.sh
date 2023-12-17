
function d() {
    local num_params=$#

    if [ $num_params -ge 2 ]; then
        local last_param=${!num_params}
        local remaining_params="${@:1:$((num_params-1))}"

        local image_tag=$(sudo docker ps -a --format "{{.Image}}" | grep -m 1 ${last_param})
        local container_id=$(sudo docker ps -aq --filter ancestor=${image_tag})

        echo "Operating on container $container_id with iamge $image_tag"
        sudo docker ${remaining_params} ${container_id}
    else
        echo "Function requires at least two parameters."
    fi
}
