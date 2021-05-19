import httplib2
import json


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
