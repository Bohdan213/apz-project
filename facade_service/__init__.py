from flask import Flask
from flask_restful import Api
import consul


consul_client = consul.Consul()

app_facade = Flask(__name__)
api_facade = Api(app_facade)