from models import Base, User
from flask import Flask, jsonify, request, url_for, abort
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()


engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# HTTPBasicAuth invokes this function when required
# to validate username & password
@auth.verify_password
def verify_password(username, password):
	user = session.query(User).filter_by(username=username).first()
	if not user or not user.verify_password(password):
		return False
	g.user = user
	return True

@app.route('/api/users', methods=['POST'])
def new_user():
	username = request.args.get('username', '')
	password = request.args.get('password', '')
	if username is None or password is None:
		abort(400)

	checkUser = session.query(User).filter_by(username=username).first()
	if checkUser:
		return jsonify({'message': f'{checkUser.username} already exists'}), 200

	user = User(username=username)
	user.hash_password(password)
	session.add(user)
	session.commit()
	return jsonify({'username': user.username}), 201
	# jsonify({'username': user.username}, 201,
	# 				'location': url_for('get_user', id=user.id),
	# 				_external=True),


# should be accessible only by logged in users
@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': f'Hello, {g.user.username}'})


@app.route('/api/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(id=id).first()
	if not user:
		abort(400)
	return jsonify({'username': user.name})


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
