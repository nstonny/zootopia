import os

import requests
from dotenv import load_dotenv


API_URL = "https://api.api-ninjas.com/v1/animals"


def fetch_data(animal_name):
	"""
	Fetches the animals data for the animal 'animal_name'.
	Returns: a list of animals, each animal is a dictionary:
	{
	  'name': ...,
	  'taxonomy': {
		...
	  },
	  'locations': [
		...
	  ],
	  'characteristics': {
		...
	  }
	},
	"""
	load_dotenv()

	name = (animal_name or "").strip()
	if not name:
		return []

	api_key = os.getenv("API_NINJAS_API_KEY")
	if not api_key:
		return []

	response = requests.get(
		API_URL,
		headers={"X-Api-Key": api_key},
		params={"name": name},
		timeout=10,
	)
	response.raise_for_status()

	animals = response.json()
	return animals if isinstance(animals, list) else []

