from app.weather_controller import (
    WeatherController,
)


def main():

    controller = (
        WeatherController()
    )

    controller.run()


if __name__ == "__main__":
    main()
