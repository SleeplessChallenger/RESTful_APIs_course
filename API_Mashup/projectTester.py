import httplib2
import sys
import json

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


address = input("Please, write desired server, else default one will be used: ")
if address == '':
	address = 'http://localhost:5000'


# Add new data ('POST')
try:
	print("Let's populate with new restaurants!")

	url = address + '/restaurants?location=Buenos+Aires+Argentina&mealType=Sushi'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

	print(json.loads(result))

	url = address + '/restaurants?location=Denver+Colorado&mealType=Soup'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

	print(json.loads(result))

	url = address + '/restaurants?location=Prague+Czech+Republic&mealType=Crepes'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

	print(json.loads(result))

	url = address + '/restaurants?location=Shanghai+China&mealType=Sandwiches'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

	print(json.loads(result))

	url = address + '/restaurants?location=Nairobi+Kenya&mealType=Pizza'
	h = httplib2.Http()
	resp, result = h.request(url, 'POST')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

	print(json.loads(result))

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test one was successfully passed')

# Receive all data ('GET')
try:
	print("Let's get all the data")
	url = address + '/restaurants'
	h = httplib2.Http()
	resp, result = h.request(url, 'GET')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")

	results = json.loads(result)
	print(results)

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test two was successfully passed')

# Retrieve specific venue (last created one)
	try:
		print('Retrieve specific restaurant')
		# think about line below
		placeID = results['restaurants'][len(results['restaurants']) - 1]['id']
		url = address + f'/restaurants/{placeID}'
		h = httplib2.Http()
		resp, result = h.request(url, 'GET')
		if resp['status'] != '200':
			raise Exception(f"{resp['status']} isn't equal to 200")
		print(json.loads(result))

	except Exception as err:
		print(err.args)
		sys.exit()

	else:
		print('Test three was successfully passed')

# Update venue
	try:
		print('Updating specific place')

		placeID = results['restaurants'][0]['id']
		url = address + f"/restaurants/{placeID}?name=Udacity&address=2465+Latham+Street+Mountain+View+CA&image=https://media.glassdoor.com/l/70/82/fc/e8/students-first.jpg"
		h = httplib2.Http()
		resp, result = h.request(url, 'PUT')
		if resp['status'] != '200':
			raise Exception(f"{resp['status']} isn't equal to 200")
		print(json.loads(result))

	except Exception as err:
		print(err.args)
		sys.exit()

	else:
		print('Test three was successfully passed')

# Delete place
try:
	print("Attempting to erase venue")

	placeID = results['restaurants'][1]['id']
	url = address + f'/restaurants/{placeID}'
	h = httplib2.Http()
	resp, result = h.request(url, 'DELETE')
	if resp['status'] != '200':
		raise Exception(f"{resp['status']} isn't equal to 200")
	print(result)

except Exception as err:
	print(err.args)
	sys.exit()

else:
	print('Test three was successfully passed')
