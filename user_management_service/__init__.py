from flask import Flask
from flask_restful import Api
import consul
from flask_sqlalchemy import SQLAlchemy
from user_management_service.services.utils import get_config, get_client
from user_management_service.controllers.queue import QueueWriter

consul_client = consul.Consul()

hz_config = get_config(consul_client, "consul-dev/hazelcast_config")
hz_client = get_client(hz_config)
messages_queue = hz_client.get_queue(hz_config["message_queue"]).blocking()
queue_writer = QueueWriter(messages_queue)

app_user_management = Flask(__name__)
api_user_management = Api(app_user_management)

app_user_management.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin_user:admin_password@localhost:5432/apz_database"

db = SQLAlchemy(app_user_management)


class User(db.Model):

    user_token = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class Group(db.Model):

    creator_token = db.Column(db.String(50), db.ForeignKey('user.user_token'))
    group_token = db.Column(db.String(50), primary_key=True)
    group_name = db.Column(db.String(50), unique=True, nullable=False)
    users_list = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Group(name={self.name})>"
