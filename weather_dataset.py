import requests
import pandas as pd


def main():

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
    )

    params = {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "start_date": "2026-04-01",
        "end_date": "2026-05-31",
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum"
        ),
        "timezone": "auto",
    }

    response = requests.get(
        url,
        params=params,
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(
        {
            "date":
                data["daily"]["time"],

            "temp_max":
                data["daily"][
                    "temperature_2m_max"
                ],

            "temp_min":
                data["daily"][
                    "temperature_2m_min"
                ],

            "precipitation":
                data["daily"][
                    "precipitation_sum"
                ],
        }
    )

    df.to_csv(
        "datasets/weather_data_apr_may.csv",
        index=False,
    )

    print(
        "Dataset saved successfully"
    )


if __name__ == "__main__":
    main()