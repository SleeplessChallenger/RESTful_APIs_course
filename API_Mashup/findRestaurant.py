import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "PASTE_YOUR_ID_HERE"
foursquare_client_secret = "YOUR_SECRET_HERE"


def getGeoCodeLocation(inputString):
	api_key = 'AIzaSyBACS3BdUU_XpYFXOCeXVZxUkqCOfeSaH0'
	finalString = inputString.replace(' ', '+')
	url = f"https://maps.googleapis.com/maps/api/geocode/json?address={finalString}={api_key}"
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result = json.loads(content)
	lat = result['results'][0]['geometry']['location']['lat']
	lon = result['results'][0]['geometry']['location']['lng']
	return (lat, lon)


def findARestaurant(mealType,location):
	lat, lon = getGeocodeLocation(location)

	url = (f'https://api.foursquare.com/v2/venues/search?client_id={foursquare_client_id}&client_secret={foursquare_client_secret}&v=20130815&ll={lat, lon}&query={mealType}')
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])

	if result['response']['venues']:
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id']
		name = restaurant['name']
		address = restaurant['location']['formattedAddress']
		output = ''

		for x in address:
			output += x + ' '
		address = output

		# url = (f"https://api.foursquare.com/v2/venues/{venue_id}/photos?client_id={foursquare_client_id}&v=20150603&client_secret={foursquare_client_secret}"
		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
		result = json.loads(h.request(url, 'GET')[1])

		if result['response']['photos']['items']:
			firstpic = result['response']['photos']['items'][0]
			prefix = firstpic['prefix']
			suffix = firstpic['suffix']
			imageURL = prefix + "300x300" + suffix
		else:
			imageURL = "https://images.unsplash.com/photo-1621145107464-c37d6b81dd58?ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwxM3x8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60"
		
		info = {'name': name, 'address': address, 'image': imageURL}
		return info
	else:
		return 'Nothing was found'


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")
