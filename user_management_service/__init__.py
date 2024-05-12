from sqlalchemy import create_engine
from flask import Flask
from flask_restful import Api
import consul
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import JSON
from user_management_service.services.utils import get_config, get_client


consul_client = consul.Consul()

hazelcast_config = get_config(consul_client, "consul-dev/hazelcast_config")
hazelcast_client = get_client(hazelcast_config)
messages_queue = hazelcast_client.get_queue(hazelcast_config["message_queue"]).blocking()

app_user_management = Flask(__name__)
api_user_management = Api(app_user_management)

Base = declarative_base()

# user_group_association = Table(
#     'user_group',
#     Base.metadata,
#     Column('user_token', Integer, ForeignKey('users.id')),
#     Column('group_token', Integer, ForeignKey('groups.id'))
# )

DATABASE_URL = "postgresql+psycopg2://admin_user:admin_password@localhost:5432/apz_database"

engine = create_engine(DATABASE_URL)
engine.connect()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):

    __tablename__ = 'users'

    user_token = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class Group(Base):

    __tablename__ = 'groups'

    creator_token = Column(Integer, ForeignKey('users.user_token'))
    group_token = Column(Integer, primary_key=True)
    group_name = Column(String(50), unique=True, nullable=False)
    users_list = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Group(name={self.name})>"
