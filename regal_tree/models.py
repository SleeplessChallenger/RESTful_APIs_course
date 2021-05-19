from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


Base = declarative_base()

# secret key can be set as .env variable
# or by the following way
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
					 for x in range(32))


class User(Base):

	__tablename__ = 'users'
	id = Column(String(32), primary_key=True)
	name = Column(String(32), index=True)
	password = Column(String(64))


	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def hash_password(self, password):
		self.password = pwd_context.hash(password)

	def get_token(self, expire=2000):
		t = Serializer(secret_key, expire)
		return t.dumps({'id': self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
		t = Serializer(secret_key)
		try:
			current = t.loads(token)['id']
		except (SignatureExpired, BadSignature):
			return None
		return User.query.get(current)


class Product(Base):

	__tablename__ = 'products'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	category = Column(String)
	price = Column(String)


	@property
	def serialize(self):
		return {
			'name': self.name,
			'category': self.category,
			'price': self.price
			}


engine = create_engine('sqlite:///regal_tree.db')
Base.metadata.create_all(engine)
