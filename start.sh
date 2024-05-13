#!/bin/bash

# Pull Consul image
docker pull consul:1.9.10

if [ ! "$(docker ps -q -f name=consul-dev)" ]; then
    docker run -d --name=consul-dev -p 8500:8500 consul:1.9.10
fi

sleep 5

#host_ip=$(hostname -I | cut -d' ' -f1)
host_ip=10.10.224.187
docker exec consul-dev consul kv put consul-dev/hazelcast_config "{\"cluster_name\": \"hazelcast-cluster\", \"cluster_members\": [\"$host_ip:5701\", \"$host_ip:5702\"], \"message_queue\": \"message_queue\"}"

if [ ! "$(docker ps -q -f name=node-1)" ]; then
    docker run -d --name node-1 --rm -e HZ_NETWORK_PUBLICADDRESS=$host_ip:5701 -e HZ_CLUSTERNAME=hazelcast-cluster -p 5701:5701 hazelcast/hazelcast:5.0
fi

if [ ! "$(docker ps -q -f name=node-2)" ]; then
    docker run -d --name node-2 --rm -e HZ_NETWORK_PUBLICADDRESS=$host_ip:5702 -e HZ_CLUSTERNAME=hazelcast-cluster -p 5702:5701 hazelcast/hazelcast:5.0
fi

docker-compose -f mongo-cluster.yml up -d

sleep 10

docker exec -it mongo1 mongosh --eval '
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" }
  ]
});
'

docker run --name apz-project-postgres \
  -e POSTGRES_USER=admin_user \
  -e POSTGRES_PASSWORD=admin_password \
  -e POSTGRES_DB=apz_database \
  -p 5432:5432 \
  -d postgres:latest

echo "Services started successfully."
