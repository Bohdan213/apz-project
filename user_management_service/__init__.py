from sqlalchemy import create_engine
from flask import Flask
from flask_restful import Api
import consul
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import JSON


consul_client = consul.Consul()

app_user_management = Flask(__name__)
api_user_management = Api(app_user_management)

Base = declarative_base()

user_group_association = Table(
    'user_group',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/apz-project"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):

    __tablename__ = 'users'

    user_token = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=True, nullable=False)

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
