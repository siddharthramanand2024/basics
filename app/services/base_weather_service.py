from app.services.weather_service import (
    WeatherService,
)


class BaseWeatherService(
    WeatherService
):

    def get_weather_data(
        self,
        latitude,
        longitude,
    ):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
        }

        data = self.fetch_weather(
            params
        )

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
