import requests


class WeatherService:

    def __init__(self):
        self.url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(self, latitude, longitude):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
        }

        response = requests.get(self.url, params=params)
        response.raise_for_status()

        data = response.json()

        current = data.get("current_weather", {})

        return {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
        }
