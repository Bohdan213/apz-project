import consul
from communication_service.services.utils import get_config, get_client

consul_client = consul.Consul(host="192.168.1.101")
hz_config = get_config(consul_client, "consul-dev/hazelcast_config")
hz_client = get_client(hz_config)
