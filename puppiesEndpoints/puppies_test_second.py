import httplib2
import json
import sys

print("Tests start now!")

address = input('Put in the desired server, otherwise default one will be used: ')
if address == '':
	address = 'http://localhost:5000'

print('Now, make a GET request')
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


print('Now, make a POST request')

try:
	url = address + '/puppies'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test two was successfully passed')


print('Start third test!')

try:
	id = 5
	while id <= 12:
		url = address + f'/puppies/{id}'
		h = httplib2.Http()
		resp, cont = h.request(url, 'GET')
		if resp['status'] != '200':
			raise Exception(f"{resp['status']} isn't equal to 200")
		id += 2

except Exception as err:
	print(err.args)
	sys.exit()
else:
	print('Test three was successfully passed')


print("Now PUT test")

try:
	id = 2
	while id <= 7:
		url = address + f"/puppies/{id}"
		h = httplib2.Http()
		resp, result = h.request(url, 'PUT')
		if resp['status'] != '200':
			raise Exception(f"{resp['status']} isn't equal to 200")
		id += 2

except Exception as err:
	print(err.args)
	sys.exit()
else:
	print('Test four was successfully passed')


print('Finally, DELETE test')

try:
	id = 2
	while id <= 7:
		url = address + f"/puppies/{id}"
		h = httplib2.Http()
		resp, result = h.request(url, 'DELETE')
		if resp['status'] != '200':
			raise Exception(f"{resp['status']} isn't equal to 200")
		id += 2

except Exception as err:
	print(err.args)
	sys.exit()
else:
	print('Test five was successfully passed')
