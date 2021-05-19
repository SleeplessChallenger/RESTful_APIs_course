from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_ap_context as pwd_context

Base = declarative_base()


class User(Base):

	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(32), index=True)
	password = Column(String(64))


	def hash_password(self, password):
		self.password = pwd_context.hash(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)


engine = create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)
