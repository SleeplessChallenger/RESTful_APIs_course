from models import Base, User, Product
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///regal_tree.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# method below implements 2 ways of
# verifying: a) by checking auth token
# b) by retrieving user from DB and 
# checking the password
@auth.verify_password
def verify_password(username_token, password):
	user = User.verify_token(username_token)

	if user:
		currentUser = session.query(User).filter_by(id=user).first()
	else:
		currentUser = session.query(User).filter_by(username=username_token).first()
		if not currentUser or currentUser.verify_password(password):
			return False

	g.user = currentUser
	return True


@app.route('/token')
@auth.login_required
def generate_token():
	t = g.user.get_token()
	return jsonify({'token': t})


@app.route('/users', methods = ['GET', 'POST'])
def register():
	name = request.json.get('name')
	password = request.json.get('password')
	if name is None or password is None:
		abort(400)

	exist = session.query(User).filter_by(name=name).first()
	if exist:
		return jsonify({'message': f'{exist.name} already registered!'}), 200

	user = User(name=name)
	user.hash_password(password)
	session.add(user)
	session.commit()
	return jsonify(User=user.serialize), 201


@app.route('/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(id=id).first()
	if not user:
		abort(400)
	return jsonify({'username': user.name})


@app.route('/resource')
@auth.login_required
def get_resource():
	return jsonify({'message': f"Hello, {g.user.name}"})


@app.route('/products', methods = ['GET', 'POST'])
@auth.login_required
def showAllBProducts():
	if request.method == 'GET':
		bagels = session.query(Product).all()
		return jsonify(Products=[i.serialize for i in bagels])

	elif request.method == 'POST':
		name = request.json.get('name')
		category = request.json.get('category')
		price = request.json.get('price')

		newItem = Product(name=name, category=category,
						  price=price)
		session.add(newItem)
		session.commit()
		return jsonify(newItem.serialize)

@app.route('/products/<str:category>')
@auth.login_required
def showCaategotyProducts(category):
	if category == 'fruit':
		fruit_items = session.query(Product).filter_by(category='fruit').all()
		return jsonify(Fruits=[i.serialize for i in fruit_items])

	if category == 'legume':
		legume_items = session.query(Product).filter_by(category='legume').all()
		return jsonify(Legume=[i.serialize for i in legume_items])

	if category == 'vegetable':
		vegetable_items = session.query(Product).filter_by(category='vegetable').all()
		return jsonify(Vegetable=[i.serialize for i in vegetable_items])


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
