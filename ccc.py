from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

engine = create_engine('sqlite:///shop.db')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tasks = relationship('Tasks', back_populates='user')

class Tasks(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('Users.id'))  # Исправлено: Integer вместо String
    user = relationship('User', back_populates='tasks')  # Исправлено: user вместо users

Base.metadata.create_all(bind=engine)
