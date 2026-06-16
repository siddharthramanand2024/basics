import argparse

from app.services.weather_service import WeatherService


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
        "--forecast-on",
        help="Forecast date (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    service = WeatherService()

    try:

        if args.location:

            latitude, longitude = (
                service.get_coordinates(args.location)
            )

        elif args.coordinates:

            latitude, longitude = (
                map(float, args.coordinates.split(","))
            )

        else:
            print(
                "Provide either --location or --coordinates"
            )
            return

        if args.forecast_on:

            forecast = service.get_forecast(
                latitude,
                longitude,
                args.forecast_on,
            )

            print(
                f"\nForecast for {forecast['date']}"
            )

            print(
                f"Max Temp: {forecast['max_temp']}°C"
            )

            print(
                f"Min Temp: {forecast['min_temp']}°C"
            )

        else:

            weather = service.get_current_weather(
                latitude,
                longitude,
            )

            print("\nCurrent Weather")

            print(
                f"Temperature: "
                f"{weather['temperature']}°C"
            )

            print(
                f"Wind Speed: "
                f"{weather['windspeed']} km/h"
            )

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
