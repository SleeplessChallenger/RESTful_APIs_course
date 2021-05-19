from models import Base, User, Product
from flask import (Flask, jsonify, request, make_response,
				   url_for, abort, g, render_template)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask.ext.httpauth import HTTPBasicAuth

# below will be imports for OAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests


app = Flask(__name__)
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///users_auth.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


clientID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']


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


@app.route('/clientOAuth')
def start():
	return render_template('clientOAuth.html')


@app.route('/token')
@auth.login_required
def generate_token():
	t = g.user.get_token()
	return jsonify({'token': t})


@app.route('/oauth/<provider>', methods = ['POST'])
def login(provider):
	# parse auth code
	auth_code = request.json.get('auth_code')
	if provider == 'google':
		# exchange for a token
		try:
			oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
			oauth_flow.redirect_uri = 'postmessage'
			credetentials = oauth_flow.step2_exchange(auth_code)

		except FlowExchangeError:
			response = make_response(json.dumps('Failure due to auth code'), 401)
			response.headers['Content-type'] = '/application/json'
			return response

		# check that token is valid
		else:
			access_token = credetentials.access_token
			url = f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}'
			h = httplib2.Http()
			result = json.loads(h.request(url, 'GET')[1])

			if result.get('error') is not None:
				response = make_response(json.dumps(result.get('error')), 500)
				response.headers['Content-type'] = 'application/json'

			# get user info
			h = httplib2.Http()
			userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
			params = {'access_token': credetentials.access_token, 'alt': 'json'}
			answer = requests.get(userinfo_url, params=params)

			data = answer.json()
			name = data['name']
			image = data['picture']
			email = data['email']

			# verify that there is no such user in DB
			# else go straight to `.get_token()`
			user = session.query(User).filter_by(email=email).first()
			if user is None:
				user = User(name=name, image=image, email=email)

				# ?? hash password

				session.add(user)
				session.commit()

			token = user.get_token()

			return jsonify({'token': token})

	else:
		return 'Unknown provider'

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


@app.route('/api/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(id=id).first()
	if not user:
		abort(400)
	return jsonify({'username': user.name})


@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({'message': f"Hello, {g.user.name}"})



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
