from sqlalchemy import create_engine
from flask import Flask
from flask_restful import Api
import consul
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


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

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), unique=True, nullable=False)
    groups = relationship('Group', secondary=user_group_association, back_populates='users')

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship('User', secondary=user_group_association, back_populates='groups')

    def __repr__(self):
        return f"<Group(name={self.name})>"