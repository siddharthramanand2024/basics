from app.services.weatherservice import WeatherService


def main():

    service = WeatherService()

    try:
        weather = service.get_current_weather(
            latitude=17.3850,
            longitude=78.4867,
        )

        print("Live Hyderabad Weather Report:")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Wind Speed: {weather['windspeed']} km/h")

    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
