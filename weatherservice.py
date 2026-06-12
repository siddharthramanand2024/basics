import requests


class WeatherService:

    def __init__(self):
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    def get_coordinates(self, city):

        response = requests.get(
            self.geo_url,
            params={"name": city, "count": 1}
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results")

        if not results:
            raise ValueError(f"Location '{city}' not found")

        return (
            results[0]["latitude"],
            results[0]["longitude"]
        )

    def get_current_weather(self, latitude, longitude):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
        }

        response = requests.get(
            self.weather_url,
            params=params
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current_weather", {})

        return {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
        }

    def get_forecast(self, latitude, longitude, forecast_date):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min",
            "start_date": forecast_date,
            "end_date": forecast_date,
            "timezone": "auto",
        }

        response = requests.get(
            self.weather_url,
            params=params
        )

        response.raise_for_status()

        data = response.json()

        daily = data.get("daily", {})

        return {
            "date": forecast_date,
            "max_temp": daily["temperature_2m_max"][0],
            "min_temp": daily["temperature_2m_min"][0],
        }