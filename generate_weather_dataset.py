

import math
import random
from datetime import date, timedelta

import pandas as pd
from faker import Faker


class WeatherDatasetGenerator:

    # City-specific climate baselines (base_temp, humidity_base, aqi_base)
    _CITY_PROFILES = {
        "Hyderabad": {"base_temp": 30.0, "humidity_base": 55, "aqi_base": 80},
        "Mumbai": {"base_temp": 28.5, "humidity_base": 70, "aqi_base": 90},
        "Delhi": {"base_temp": 25.0, "humidity_base": 45, "aqi_base": 150},
        "Bangalore": {"base_temp": 24.0, "humidity_base": 60, "aqi_base": 65},
        "Chennai": {"base_temp": 29.0, "humidity_base": 68, "aqi_base": 75},
    }

    def __init__(self, seed=42):
        self.faker = Faker("en_IN")
        Faker.seed(seed)
        random.seed(seed)

        self.cities = list(self._CITY_PROFILES.keys())
        self.start_date = date(2025, 1, 1)
        self.end_date = date(2025, 12, 31)
        self.dataset = None

    def _get_seasonal_factor(self, current_date):

        day_of_year = current_date.timetuple().tm_yday
        # Peak around day 150 (end of May)
        return 6.0 * math.sin(
            2 * math.pi * (day_of_year - 80) / 365
        )

    def _get_time_of_day_factor(self, hour):
        return 5.0 * math.sin(
            2 * math.pi * (hour - 5) / 24
        )

    def _is_monsoon(self, current_date):

        return current_date.month in (6, 7, 8, 9)

    def _generate_temperature(self, city, current_date, hour):

        base = self._CITY_PROFILES[city]["base_temp"]
        seasonal = self._get_seasonal_factor(current_date)
        time_adj = self._get_time_of_day_factor(hour)
        noise = random.gauss(0, 1.5)

        temperature = base + seasonal + time_adj + noise
        return round(max(5.0, min(48.0, temperature)), 1)

    def _generate_humidity(self, city, current_date, temperature):

        base = self._CITY_PROFILES[city]["humidity_base"]
        # Higher temp → lower humidity
        temp_effect = -0.8 * (temperature - 30)
        # Monsoon boost
        monsoon_boost = 20 if self._is_monsoon(current_date) else 0
        noise = random.gauss(0, 5)

        humidity = base + temp_effect + monsoon_boost + noise
        return int(max(15, min(100, humidity)))

    def _generate_wind_speed(self, current_date):

        base = 8.0
        monsoon_boost = 6.0 if self._is_monsoon(current_date) else 0
        noise = random.gauss(0, 3)

        wind_speed = base + monsoon_boost + noise
        return round(max(0.0, min(50.0, wind_speed)), 1)

    def _generate_pressure(self, temperature):

        base = 1013.0
        temp_effect = -0.3 * (temperature - 30)
        noise = random.gauss(0, 3)

        pressure = base + temp_effect + noise
        return round(max(995.0, min(1030.0, pressure)), 1)

    def _generate_rainfall(self, current_date, humidity):

        if self._is_monsoon(current_date):
            rain_probability = 0.25
        elif current_date.month in (10, 11):
            rain_probability = 0.10
        else:
            rain_probability = 0.03

        # High humidity increases rain chance
        if humidity > 80:
            rain_probability *= 1.5

        if random.random() < rain_probability:
            return round(random.uniform(0.1, 25.0), 1)
        return 0.0

    def _generate_uv_index(self, hour, current_date):
        if hour < 6 or hour > 18:
            return 0

        # Peak at noon
        hour_factor = max(
            0, 1 - abs(hour - 12) / 6
        )
        # Seasonal factor: higher in summer
        day_of_year = current_date.timetuple().tm_yday
        seasonal = 0.8 + 0.2 * math.sin(
            2 * math.pi * (day_of_year - 80) / 365
        )
        # Cloud cover during monsoon reduces UV
        monsoon_reduction = 0.6 if self._is_monsoon(current_date) else 1.0

        uv = 12 * hour_factor * seasonal * monsoon_reduction
        noise = random.gauss(0, 0.5)
        return int(max(0, min(12, uv + noise)))

    def _generate_air_quality(self, city, current_date, hour):
        base = self._CITY_PROFILES[city]["aqi_base"]

        # Winter inversion effect (Nov-Feb)
        if current_date.month in (11, 12, 1, 2):
            winter_boost = 40
        else:
            winter_boost = 0

        # Rush hour effect (8-10 AM, 5-8 PM)
        if hour in (8, 9, 10, 17, 18, 19, 20):
            rush_boost = 15
        else:
            rush_boost = 0

        # Monsoon cleans air
        monsoon_effect = -25 if self._is_monsoon(current_date) else 0

        noise = random.gauss(0, 12)
        aqi = base + winter_boost + rush_boost + monsoon_effect + noise
        return int(max(20, min(400, aqi)))

    def generate_dataset(self):
        records = []
        total_days = (self.end_date - self.start_date).days + 1

        for day_offset in range(total_days):
            current_date = self.start_date + timedelta(days=day_offset)
            date_str = current_date.strftime("%Y-%m-%d")

            for hour in range(24):
                time_str = f"{hour:02d}:00"
                # Rotate cities across hours to get even distribution
                city = self.cities[
                    (day_offset * 24 + hour) % len(self.cities)
                ]

                temperature = self._generate_temperature(
                    city, current_date, hour
                )
                humidity = self._generate_humidity(
                    city, current_date, temperature
                )
                wind_speed = self._generate_wind_speed(current_date)
                pressure = self._generate_pressure(temperature)
                rainfall = self._generate_rainfall(
                    current_date, humidity
                )
                uv_index = self._generate_uv_index(hour, current_date)
                air_quality = self._generate_air_quality(
                    city, current_date, hour
                )

                records.append({
                    "date": date_str,
                    "time": time_str,
                    "city": city,
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "pressure": pressure,
                    "rainfall": rainfall,
                    "uv_index": uv_index,
                    "air_quality": air_quality,
                })

        self.dataset = pd.DataFrame(records)
        print(
            f"Generated {len(self.dataset)} records "
            f"from {self.start_date} to {self.end_date}"
        )
        return self.dataset

    def save_dataset(self, filepath="datasets/weather_dataset.csv"):

        if self.dataset is None:
            raise ValueError(
                "No dataset to save. Call generate_dataset() first."
            )

        self.dataset.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        print(f"Shape: {self.dataset.shape}")
        print(f"Columns: {list(self.dataset.columns)}")


def main():
    generator = WeatherDatasetGenerator(seed=42)
    generator.generate_dataset()
    generator.save_dataset()


if __name__ == "__main__":
    main()
