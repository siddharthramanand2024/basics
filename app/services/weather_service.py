import requests

from abc import (
    ABC,
    abstractmethod,
)


class WeatherService(
    ABC
):

    def __init__(self):

        self._weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

    def fetch_weather(
        self,
        params,
    ):

        response = requests.get(
            self._weather_url,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    @abstractmethod
    def get_weather_data(
        self,
        *args,
        **kwargs,
    ):
        pass
