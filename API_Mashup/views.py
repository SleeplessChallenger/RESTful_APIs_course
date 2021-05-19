from findRestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


engine = create_engine('sqlite:///restaurant.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

foursquare_client_id = 'ENTER_YOUR_CREDETENTIALS'
foursquare_client_secret = 'ENTER_YOUR_CREDETENTIALS'
google_api_key = 'ENTER_YOUR_CREDETENTIALS'


@app.route('/restaurants', methods=['GET', 'POST'])
def restaurantsAll():
	if request.method == 'GET':
		return getInfo()

	elif request.method == 'POST':
		loc = request.args.get('location', '')
		meal = request.args.get('mealType', '')
		return addInfo(loc, meal)


@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurantHandler(id):
	if request.method == 'GET':
		return getParticularPlace(id)

	elif request.method == 'PUT':
		name = request.args.get('name', '')
		loc = request.args.get('location', '')
		image = request.args.get('image', '')
		return updatePlace(name, loc, image, id)

	elif request.method == 'DELETE':
		return eraseVenue(id)


def getInfo():
	venues = session.query(Restaurant).all()
	return jsonify(AllPlaces=[i.serialize for i in venues])

def addInfo(loc, meal):
	result = findARestaurant(meal, loc)
	if result != 'Nothing was found':
		restaurantDB = Restaurant(name=unicode(result['name']), address=unicode(result['address']),
								  image=result['image'])
		session.add(restaurantDB)
		session.commit()
		return jsonify(NewVenue=restaurantDB.serialize)
	else:
		return jsonify({'Error': 'No venues were found'})

def getParticularPlace(id):
	venue = session.query(Restaurant).filter_by(id=id).first()
	return jsonify(Venue=venue.serialize)

def updatePlace(name, loc, image, id):
	venue = session.query(Restaurant).filter_by(id=id).first()
	if name:
		venue.name = name
	if loc:
		venue.address = loc
	if image:
		venue.image = image
	# when updating there is no need in `add`
	session.commit()
	return jsonify(Place=venue.serialize)

def eraseVenue(id):
	venue = session.query(Restaurant).filter_by(id=id).first()
	session.delete(venue)
	session.commit()
	return jsonify({'message': 'Venue was deleted'})


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
