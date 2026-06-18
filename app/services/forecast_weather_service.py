from datetime import (
    datetime,
    timedelta,
)

from app.services.weather_service import (
    WeatherService,
)


class ForecastWeatherService(
    WeatherService
):

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

        data = self.fetch_weather(
            params
        )

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
