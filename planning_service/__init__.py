from flask import Flask
from flask_restful import Api
import consul
from planning_service.services.utils import get_config, get_client


consul_client = consul.Consul()

hazelcast_config = get_config(consul_client, "consul-dev/hazelcast_config")
hazelcast_client = get_client(hazelcast_config)
messages_queue = hazelcast_client.get_queue(hazelcast_config["message_queue"]).blocking()

app_planning = Flask(__name__)
api_planning = Api(app_planning)