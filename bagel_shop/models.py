from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Bagel(Base):

	__tablename__ = 'bagels'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	picture = Column(String)
	description = Column(String)
	price = Column(String)
	


	@property
	def serialize(self):
		return {
			'name': self.name,
			'picture': self.picture,
			'description': self.description,
			'price': self.price
			}


class User(Base):

	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)
	password = Column(String(64))


	@property
	def serialize(self):
		return {
			'name': self.name
		}
	


	def hash_password(self, password):
		self.password = pwd_context.hash(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)


engine = create_engine('sqlite:///bagel_shop.db')

Base.metadata.create_all(engine)
