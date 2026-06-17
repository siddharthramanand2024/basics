import argparse
from datetime import datetime

from app.services.weather_service import WeatherService
from app.services.geo_service import GeoService

from app.exceptions import (
    InvalidCoordinateException,
    InvalidDateException,
    InvalidLocationException,
)


def validate_coordinates(
    latitude,
    longitude,
):

    if not (-90 <= latitude <= 90):
        raise InvalidCoordinateException(
            "Latitude must be between -90 and 90"
        )

    if not (-180 <= longitude <= 180):
        raise InvalidCoordinateException(
            "Longitude must be between -180 and 180"
        )


def validate_date(
    date_string,
):

    try:

        requested_date = datetime.strptime(
            date_string,
            "%Y-%m-%d",
        ).date()

    except ValueError:

        raise InvalidDateException(
            "Date must be in YYYY-MM-DD format"
        )

    if requested_date < datetime.today().date():

        raise InvalidDateException(
            "Past dates are not allowed"
        )


def main():

    parser = argparse.ArgumentParser(
        description="Weather CLI Application"
    )

    parser.add_argument(
        "--location",
        help="City name"
    )

    parser.add_argument(
        "--coordinates",
        help="latitude,longitude"
    )

    parser.add_argument(
        "--date",
        help="Forecast date (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--forecast",
        help="Number of forecast days (example: 2days)"
    )

    args = parser.parse_args()

    weather_service = WeatherService()
    geo_service = GeoService()

    try:

        location_name = None

        if args.location:

            location_name = args.location

            latitude, longitude = (
                geo_service.get_coordinates(
                    args.location
                )
            )

        elif args.coordinates:

            try:

                latitude, longitude = map(
                    float,
                    args.coordinates.split(",")
                )

            except ValueError:

                raise InvalidCoordinateException(
                    "Coordinates must be in latitude,longitude format"
                )

            validate_coordinates(
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

            validate_date(args.date)

            forecast_days = 1

            if args.forecast:

                try:

                    forecast_days = int(
                        args.forecast.replace(
                            "days",
                            ""
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
                weather_service.get_forecast(
                    latitude,
                    longitude,
                    args.date,
                    forecast_days,
                )
            )

            print(
                f"Location: {location_name}"
            )

            print("\nForecast")
            print("--------")

            for forecast in forecasts:

                print(
                    f"\nDate     : {forecast['date']}"
                )

                print(
                    f"Max Temp : "
                    f"{forecast['max_temp']}°C"
                )

                print(
                    f"Min Temp : "
                    f"{forecast['min_temp']}°C"
                )

        else:

            weather = (
                weather_service
                .get_current_weather(
                    latitude,
                    longitude,
                )
            )

            print(
                f"Location: {location_name}"
            )

            print("\nCurrent Weather")
            print("---------------")

            print(
                f"Temperature : "
                f"{weather['temperature']}°C"
            )

            print(
                f"Wind Speed  : "
                f"{weather['windspeed']} km/h"
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


if __name__ == "__main__":
    main()