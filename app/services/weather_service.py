import requests


class WeatherService:

    def __init__(self):

        self.weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

    def fetch_weather(
        self,
        params,
    ):

        response = requests.get(
            self.weather_url,
            params=params,
        )

        response.raise_for_status()

        return response.json()
