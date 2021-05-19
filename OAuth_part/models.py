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


class User:

	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(32), index=True)
	image = Column(String)
	email = Column(String)
	password = Column(String(64))


	def hash_password(self, password):
		self.password = pwd_context.hash(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def get_token(self, expires=1500):
		t = Serializer(secret_key, expires)
		return t.dumps({'id': self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
		t = Serializer(secret_key)
		try:
			temp = t.loads(token)['id']
		except (BadSignature, SignatureExpired):
			return None
		else:
			return temp


engine = create_engine('sqlite:///users_auth.db')
Base.metadata.create_all(engine)
