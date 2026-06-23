import argparse

from app.validators import Validator

from app.services.geo_service import GeoService

from app.services.base_weather_service import (
    BaseWeatherService,
)

from app.services.forecast_weather_service import (
    ForecastWeatherService,
)

from app.exceptions import (
    InvalidCoordinateException,
    InvalidDateException,
    InvalidLocationException,
)


class WeatherController:

    def __init__(self):

        self.geo_service = GeoService()

        self.current_weather_service = (
            BaseWeatherService()
        )

        self.forecast_weather_service = (
            ForecastWeatherService()
        )

    def run(self):

        parser = argparse.ArgumentParser(
            description="Weather CLI Application"
        )

        parser.add_argument(
            "--location",
            help="City name",
        )

        parser.add_argument(
            "--coordinates",
            help="latitude,longitude",
        )

        parser.add_argument(
            "--date",
            help="Forecast date (YYYY-MM-DD)",
        )

        parser.add_argument(
            "--forecast",
            help="Number of forecast days (example: 2days)",
        )

        args = parser.parse_args()

        try:

            location_name = None

            if args.location:

                location_name = args.location

                latitude, longitude = (
                    self.geo_service.get_coordinates(
                        args.location
                    )
                )

            elif args.coordinates:

                try:

                    latitude, longitude = map(
                        float,
                        args.coordinates.split(","),
                    )

                except ValueError:

                    raise InvalidCoordinateException(
                        "Coordinates must be in latitude,longitude format"
                    )

                Validator.validate_coordinates(
                    latitude,
                    longitude,
                )

                location_name = (
                    f"{latitude}, {longitude}"
                )

            else:

                raise InvalidLocationException(
                    "Provide either --location or --coordinates"
                )

            if args.date:

                Validator.validate_date(
                    args.date
                )

                forecast_days = 1

                if args.forecast:

                    try:

                        forecast_days = int(
                            args.forecast.replace(
                                "days",
                                "",
                            )
                        )

                    except ValueError:

                        raise InvalidDateException(
                            "Forecast must be in format like 2days"
                        )

                    if forecast_days <= 0:

                        raise InvalidDateException(
                            "Forecast days must be greater than 0"
                        )

                forecasts = (
                    self.forecast_weather_service
                    .get_weather_data(
                        latitude,
                        longitude,
                        args.date,
                        forecast_days,
                    )
                )

                self.print_forecast(
                    location_name,
                    forecasts,
                )

            else:

                weather = (
                    self.current_weather_service
                    .get_weather_data(
                        latitude,
                        longitude,
                    )
                )

                self.print_current_weather(
                    location_name,
                    weather,
                )

        except InvalidLocationException as error:

            print(
                f"Location Error: {error}"
            )

        except InvalidCoordinateException as error:

            print(
                f"Coordinate Error: {error}"
            )

        except InvalidDateException as error:

            print(
                f"Date Error: {error}"
            )

        except Exception as error:

            print(
                f"Unexpected Error: {error}"
            )

    def print_current_weather(
        self,
        location_name,
        weather,
    ):

        print(
            f"Location : {location_name}"
        )

        print(
            "\nCurrent Weather"
        )

        print(
            "---------------"
        )

        print(
            f"Temperature : "
            f"{weather['temperature']}°C"
        )

        print(
            f"Wind Speed  : "
            f"{weather['windspeed']} km/h"
        )

    def print_forecast(
        self,
        location_name,
        forecasts,
    ):

        print(
            f"Location : {location_name}"
        )

        print(
            "\nForecast"
        )

        print(
            "--------"
        )

        for forecast in forecasts:

            print(
                f"\nDate     : "
                f"{forecast['date']}"
            )

            print(
                f"Max Temp : "
                f"{forecast['max_temp']}°C"
            )

            print(
                f"Min Temp : "
                f"{forecast['min_temp']}°C"
            )
