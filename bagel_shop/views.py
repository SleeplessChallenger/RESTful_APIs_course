from models import Base, User, Bagel
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()

engine = create_engine('sqlite:///bagel_shop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@auth.verify_password
def verify_password(username, password):
	user = session.query(User).filter_by(name=username).first()
	if user is None or not user.verify_password(password):
		return False
	g.user = user
	return True

@app.route('/users', methods = ['GET', 'POST'])
def register():
	name = request.post.get('name')
	password = request.post.get('password')
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


@app.route('/bagels', methods = ['GET', 'POST'])
@auth.login_required
def showAllBagels():
	if request.method == 'GET':
		bagels = session.query(Bagel).all()
		return jsonify(Bagels=[i.serialize for i in bagels])

	elif request.method == 'POST':
		name = request.json.get('name')
		descr = request.json.get('description')
		picture = request.json.get('picture')
		price = request.json.get('price')
		newItem = Bagel(name=name, picture=picture,
						description=descr,
						price=price)
		session.add(newItem)
		session.commit()
		return jsonify(newItem.serialize)


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
