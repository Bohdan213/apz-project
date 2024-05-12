#!/bin/bash

# Pull Consul image
docker pull consul:1.9.10

# Run Consul container if it doesn't exist
if [ ! "$(docker ps -q -f name=consul-dev)" ]; then
    docker run -d --name=consul-dev -p 8500:8500 consul:1.9.10
fi

# Wait for Consul container to start
sleep 5

# Get host IP address
#host_ip=$(hostname -I | cut -d' ' -f1)
host_ip=10.10.224.187
# Set Consul key-value pair with correct IP addresses
docker exec consul-dev consul kv put consul-dev/hazelcast_config "{\"cluster_name\": \"hazelcast-cluster\", \"cluster_members\": [\"$host_ip:5701\", \"$host_ip:5702\"], \"message_queue\": \"msg\"}"

# Run Hazelcast nodes if they don't exist
if [ ! "$(docker ps -q -f name=node-1)" ]; then
    docker run -d --name node-1 --rm -e HZ_NETWORK_PUBLICADDRESS=$host_ip:5701 -e HZ_CLUSTERNAME=hazelcast-cluster -p 5701:5701 hazelcast/hazelcast:5.0
fi

if [ ! "$(docker ps -q -f name=node-2)" ]; then
    docker run -d --name node-2 --rm -e HZ_NETWORK_PUBLICADDRESS=$host_ip:5702 -e HZ_CLUSTERNAME=hazelcast-cluster -p 5702:5701 hazelcast/hazelcast:5.0
fi

echo "Services started successfully."
