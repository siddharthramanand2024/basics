import requests

from app.exceptions import (
    InvalidLocationException,
)


class GeoService:

    def __init__(self):

        self._geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

    def get_coordinates(
        self,
        location,
    ):

        response = requests.get(
            self._geo_url,
            params={
                "name": location,
                "count": 1,
            },
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "results"
        )

        if not results:

            raise InvalidLocationException(
                f"Location '{location}' not found"
            )

        return (
            results[0]["latitude"],
            results[0]["longitude"],
        )
