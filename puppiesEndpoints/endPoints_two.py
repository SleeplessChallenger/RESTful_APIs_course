from flask import Flask, request


app = Flask(__name__)


@app.route('/puppies', methods = ['GET', 'POST'])
def puppiesFunction():
	if request.method == 'GET':
		return getAllPuppies()
	elif request.method == 'POST':
		return makeANewPuppy()


@app.route('/puppies/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):
	if request.method == 'GET':
		return getPuppy(id)

	if request.method == 'PUT':
		return updatePuppy(id)

	elif request.method == 'DELETE':
		return deletePuppy(id)


def getAllPuppies():
  return "Getting All the puppies!"
  
def makeANewPuppy():
  return "Creating A New Puppy!"

def getPuppy(id):
	return f"Getting Puppy with id {id}"
	
def updatePuppy(id):
  return f"Updating a Puppy with id {id}"

def deletePuppy(id):
  return f"Removing Puppy with id {id}"


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
