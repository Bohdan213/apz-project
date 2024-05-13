import random
from flask import Flask
from flask_restful import Api
import consul
from facade_service.services.utils import get_config, get_client

consul_client = consul.Consul()

hz_config = get_config(consul_client, "consul-dev/hazelcast_config")
hz_client = get_client(hz_config)

def get_url(service_name):
    _, services = consul_client.health.service(service_name, passing=True)
    if not services:
        return None
    return [f"http://{service['Node']['Address']}:{service['Service']['Port']}" for service in services]

def get_random_url(service_name):
    urls = get_url(service_name)
    if not urls:
        return None
    url_to_send = random.choice(urls)
    if service_name == "user_management_service":
        return url_to_send + "/api/v1/user_management_service"
    if service_name == "planning_service":
        return url_to_send + "/api/v1/planning_service"
    return random.choice(urls)

# def parse_

app_facade = Flask(__name__)
api_facade = Api(app_facade)