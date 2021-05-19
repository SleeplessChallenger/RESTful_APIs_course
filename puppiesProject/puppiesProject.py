from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Puppy


engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


@app.route('/')
@app.route('/puppies', methods = ['GET', 'POST'])
def puppiesFunction():
	if request.method == 'GET':
		return getAllPuppies()

	elif request.method == 'POST':
		name = request.args.get('name', '')
		descr = request.args.get('description', '')
		return makeANewPuppy(name, descr)


@app.route('/puppies/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):
	if request.method == 'GET':
		return getPuppy(id)

	elif request.method == 'PUT':
		name = request.args.get('name', '')
		descr = request.args.get('description', '')
		return updatePuppy(id, name, descr)

	elif request.method == 'DELETE':
		return deletePuppy(id)


def getAllPuppies():
	items = session.query(Puppy).all()
	return jsonify(All_Puppies=[i.serialize for i in items])

def getPuppy(id):
	item = session.query(Puppy).filter_by(id=id).first()
	return jsonify(Puppy=item.serialize)
  
def makeANewPuppy(name, description):
	puppy = Puppy(name = name, description = description)
	session.add(puppy)
	session.commit()
	return jsonify(Puppy=puppy.serialize)

def updatePuppy(id, name, descr):
	puppy = session.query(Puppy).filter_by(id=id).first()
	if name:
		puppy.name = name
	if descr:
		puppy.description = descr
	session.add(puppy)
	session.commit()
	return f"Updated puppy with id: {id}"

def deletePuppy(id):
	puppy = session.query(Puppy).filter_by(id=id).first()
	session.delete(puppy)
	session.commit()
	return f"Removing Puppy with id {id}"


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
