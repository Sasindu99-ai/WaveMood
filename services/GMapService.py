from os import environ

import requests

from vvecon.qt.logger import logger

__all__ = ['GMapService']


class GMapService:
	_API_KEY: str = environ.get('GOOGLE_MAPS_API_KEY', 'AIzaSyD2Wty15KnL8TSbj3BMR_DK9G33sEMbQAI')
	BASE_URL = 'https://maps.googleapis.com/maps/api/'

	def callAPI(self, action: str, params: dict) -> dict:
		params['key'] = self._API_KEY
		url = f'{self.BASE_URL}{action}'

		try:
			logger.info(f'Calling Google Maps API: {url} {params}')
			response = requests.get(url, params=params, timeout=10)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			errorMsg = f'Error calling Google Maps API: {e}'
			logger.error(errorMsg)

	def autoComplete(
		self,
		query: str,
		components: str | None = None,
		placeType: str | None = None,
	) -> dict:
		params = dict(input=query)
		if components:
			params['components'] = components
		if placeType:
			params['type'] = placeType
		return self.callAPI('place/autocomplete/json', params)

	def locationInfo(self, placeId: str) -> dict:
		params = dict(place_id=placeId)
		return self.callAPI('place/details/json', params)

	def distance(self, origin: dict, destination: dict) -> dict:
		params = dict(
			origins=f"{origin.get('lat')},{origin.get('lng')}",
			destinations=f"{destination.get('lat')},{destination.get('lng')}",
		)
		return self.callAPI('distancematrix/json', params)

	@staticmethod
	def generate_squares(lat_min, lat_max, lng_min, lng_max, step):
		"""
		Generate square coordinates for a given area.
		:param lat_min: Minimum latitude.
		:param lat_max: Maximum latitude.
		:param lng_min: Minimum longitude.
		:param lng_max: Maximum longitude.
		:param step: Step size for dividing the area (in degrees).
		:return: List of square coordinates [(lat1, lng1, lat2, lng2), ...].
		"""
		squares = []
		lat = lat_min
		while lat < lat_max:
			lng = lng_min
			while lng < lng_max:
				squares.append((lat, lng, lat + step, lng + step))
				lng += step
			lat += step
		return squares

	def searchBusinesses(self, location: str, radius: int, query: str) -> list[dict]:
		"""
		Search for businesses in a specific location.
		:param location: Latitude and longitude as a string (e.g., "6.9271,79.8612").
		:param radius: Search radius in meters.
		:param query: Search text.
		:return: List of businesses.
		"""
		params = dict(location=location, radius=radius, query=query)
		response = self.callAPI('place/textsearch/json', params)
		return response.get('results', [])