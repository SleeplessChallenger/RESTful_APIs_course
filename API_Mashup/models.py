from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):

	__tablename__ = 'restaurants'

	id = Column(Integer, primary_key=True)
	name = Column(String(75), nullable=False)
	address = Column(String)
	image = Column(String)


	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'address': self.address,
			'image': self.image
		}


engine = create_engine('sqlite:///restaurant.db')
Base.metadata.create_all(engine)
