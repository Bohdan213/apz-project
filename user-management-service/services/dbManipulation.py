


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    # Relationship to Group using association table
    groups = relationship('Group', secondary=user_group_association, back_populates='users')

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relationship to User using association table
    users = relationship('User', secondary=user_group_association, back_populates='groups')

    def __repr__(self):
        return f"<Group(name={self.name})>"