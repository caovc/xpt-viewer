#!/usr/bin/env bash

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Get the container name
container_name=xport-viewer

# Check if the container exists
if docker ps -a | grep -Fq "$container_name"; then
    echo "Container $container_name exists, stopping and deleting it..."

    # Stop the container
    docker stop "$container_name"

    # Delete the container
    docker rm "$container_name"

    # Delete the container's image
    docker rmi "$container_name"

    echo "Container $container_name has been stopped and deleted."
else
    echo "Container $container_name does not exist."
fi

docker build -t "xport-viewer" .
docker run -itd -p 4000:80 -v /opt/xpt-viewer:/app --restart=always  --name=xport-viewer xport-viewer