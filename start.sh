#MYIP=10.10.224.187

docker pull consul:1.9.10

docker run -d --name=consul-dev -p 8500:8500 consul:1.9.10

docker exec -it consul-dev sh

consul kv put consul-dev/hazelcast_config '{"cluster_name": "hazelcast-cluster", "cluster_members": ["$(MYIP):5701", "$(MYIP):5702"], "message_queue": "msg"}' &

docker run \
    -it \
    --name node-1 --rm \
    -e HZ_NETWORK_PUBLICADDRESS=10.10.224.187:5701 \
    -e HZ_CLUSTERNAME=hazelcast-cluster \
    -p 5701:5701 hazelcast/hazelcast:5.0 &

docker run \
    -it \
    --name node-2 --rm \
    -e HZ_NETWORK_PUBLICADDRESS=10.10.224.187:5702 \
    -e HZ_CLUSTERNAME=hazelcast-cluster \
    -p 5702:5701 hazelcast/hazelcast:5.0