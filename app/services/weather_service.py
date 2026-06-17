import requests
from datetime import datetime, timedelta


class WeatherService:

    def __init__(self):

        self.weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

    def get_current_weather(
        self,
        latitude,
        longitude,
    ):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
        }

        response = requests.get(
            self.weather_url,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        current = data.get(
            "current_weather",
            {},
        )

        return {
            "temperature": current.get(
                "temperature"
            ),
            "windspeed": current.get(
                "windspeed"
            ),
        }

    def get_forecast(
        self,
        latitude,
        longitude,
        start_date,
        days=1,
    ):

        start = datetime.strptime(
            start_date,
            "%Y-%m-%d",
        ).date()

        end = start + timedelta(
            days=days - 1
        )

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min"
            ),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "timezone": "auto",
        }

        response = requests.get(
            self.weather_url,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        daily = data.get(
            "daily",
            {},
        )

        forecasts = []

        for index in range(
            len(daily["time"])
        ):

            forecasts.append(
                {
                    "date":
                        daily["time"][index],
                    "max_temp":
                        daily[
                            "temperature_2m_max"
                        ][index],
                    "min_temp":
                        daily[
                            "temperature_2m_min"
                        ][index],
                }
            )

        return forecasts
