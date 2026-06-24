import requests
import pandas as pd


URL = (
    "https://archive-api.open-meteo.com/v1/archive"
)

params = {
    "latitude": 17.3850,
    "longitude": 78.4867,
    "start_date": "2025-04-01",
    "end_date": "2025-05-31",
    "hourly": "temperature_2m",
    "timezone": "auto",
}

response = requests.get(
    URL,
    params=params,
)

response.raise_for_status()

data = response.json()

times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]

rows = {}

for time_value, temp in zip(
    times,
    temps,
):

    date_part, hour_part = (
        time_value.split("T")
    )

    hour = int(
        hour_part.split(":")[0]
    )

    if date_part not in rows:

        rows[date_part] = {
            "date": date_part
        }

    rows[date_part][
        f"{hour}-hour"
    ] = temp

df = pd.DataFrame(
    rows.values()
)

df.to_csv(
    "datasets/hourly_weather_dataset.csv",
    index=False,
)

print(
    "Dataset generated successfully"
)