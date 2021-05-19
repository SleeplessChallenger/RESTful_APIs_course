import httplib2
import json
import sys

print("Tests start now!")

address = input('Put in the desired server, otherwise default one will be used: ')
if address == '':
	address = 'http://localhost:5000'

print('At first, make a GET request')
try:
	url = address + '/puppies'
	h = httplib2.Http()
	resp, result = h.request(url, 'GET')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test one was successfully passed')


print('Make a POST request')

try:
	url = address + '/puppies?name=Zuki&description=Playful+Little+Puppy'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	# print(json.loads(result).items())
	obj = json.loads(result)
	puppyID = obj['Puppy']['id']
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test two was successfully passed')


print('After POST, make another GET request')
try:
	id = puppyID
	url = address + f'/puppies/{id}'
	h = httplib2.Http()
	resp, result = h.request(url, 'GET')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test one was successfully passed')


print("Now PUT test")

try:
	id = puppyID
	url = address + f"/puppies/{id}?name=Miyamo&description=A+sleepy+bundle+of+joy"
	h = httplib2.Http()
	resp, result = h.request(url, 'PUT')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

except Exception as err:
	print(err.args)
	sys.exit()
else:
	print('Test four was successfully passed')


print('Finally, DELETE test')

try:
	id = puppyID
	url = address + f"/puppies/{id}"
	h = httplib2.Http()
	resp, result = h.request(url, 'DELETE')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

except Exception as err:
	print(err.args)
	sys.exit()
else:
	print('Test five was successfully passed')
