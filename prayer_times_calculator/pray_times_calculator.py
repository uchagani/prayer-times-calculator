from datetime import datetime

import requests

from .exceptions import CalculationMethodError, InvalidResponseError


class PrayerTimesCalculator:

    API_URL = "http://api.aladhan.com/timings"

    CALCULATION_METHODS = {
        "karachi": 1,
        "isna": 2,
        "mwl": 3,
        "makkah": 4,
        "egypt": 5,
        "tehran": 7,
        "gulf": 8,
        "kuwait": 9,
        "qatar": 10,
        "singapore": 11,
        "france": 12,
        "turkey": 13,
        "russia": 14,
    }

    SCHOOLS = {"shafi": 0, "hanafi": 1}
    MIDNIGHT_MODES = {"standard": 0, "jafari": 1}
    LAT_ADJ_METHODS = {"middle of the night": 1, "one seventh": 2, "angle based": 3}

    def __init__(
        self,
        latitude: float,
        longitude: float,
        calculation_method: str,
        date: str,
        school="",
        midnightMode="",
        latitudeAdjustmentMethod="",
    ):

        if calculation_method.lower() not in self.CALCULATION_METHODS:
            raise CalculationMethodError(
                "\nInvalid Calculation Method.  Must "
                "be one of: {}".format(", ".join(self.CALCULATION_METHODS.keys()))
            )
        if school and school.lower() not in self.SCHOOLS:
            raise CalculationMethodError(
                "\nInvalid School. Must "
                "be one of: {}".format(", ".join(self.SCHOOLS.keys()))
            )
        if midnightMode and midnightMode.lower() not in self.MIDNIGHT_MODES:
            raise CalculationMethodError(
                "\nInvalid midnightMode. Must "
                "be one of: {}".format(", ".join(self.MIDNIGHT_MODES.keys()))
            )
        if (
            latitudeAdjustmentMethod
            and latitudeAdjustmentMethod.lower() not in self.LAT_ADJ_METHODS
        ):
            raise CalculationMethodError(
                "\nInvalid latitudeAdjustmentMethod. Must "
                "be one of: {}".format(", ".join(self.LAT_ADJ_METHODS.keys()))
            )

        self._latitude = latitude
        self._longitude = longitude
        self._calculation_method = self.CALCULATION_METHODS[calculation_method.lower()]
        self._school = self.SCHOOLS.get(school.lower())
        self._midnight_mode = self.MIDNIGHT_MODES.get(midnightMode.lower())
        self._lat_adj_method = self.LAT_ADJ_METHODS.get(
            latitudeAdjustmentMethod.lower()
        )

        date_parsed = datetime.strptime(date, "%Y-%m-%d")
        self._timestamp = int(date_parsed.timestamp())

    def fetch_prayer_times(self):
        """Return prayer times for defined parameters."""
        url = f"{self.API_URL}/{self._timestamp}"
        params = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "method": self._calculation_method,
        }
        if self._school:
            params.update({"school": self._school})
        if self._midnight_mode:
            params.update({"midnightMode": self._midnight_mode})
        if self._lat_adj_method:
            params.update({"latitudeAdjustmentMethod": self._lat_adj_method})

        response = requests.get(url, params=params)

        if not response.status_code == 200:
            raise InvalidResponseError(f"\nUnable to retrive prayer times. Url: {url}")

        return response.json()["data"]["timings"]
