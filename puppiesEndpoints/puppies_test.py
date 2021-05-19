import httplib2
import json
import sys

print("Start first test!")

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


print('Start second test!')

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
	print('Test two was successfully passed')
