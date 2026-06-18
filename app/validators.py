from datetime import datetime

from app.exceptions import (
    InvalidCoordinateException,
    InvalidDateException,
)


class Validator:

    @staticmethod
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

    @staticmethod
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
