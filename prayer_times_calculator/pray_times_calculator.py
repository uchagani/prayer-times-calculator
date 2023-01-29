from datetime import datetime

import requests

from .exceptions import CalculationMethodError, InvalidResponseError


class PrayerTimesCalculator:

    API_URL = "http://api.aladhan.com/v1/timings"

    CALCULATION_METHODS = {
        "jafari": 0,
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
        "moonsighting": 15,
        "custom": 99,
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
        tune = bool,
        imsak_tune = 0,
        fajr_tune = 0,
        sunrise_tune = 0,
        dhuhr_tune = 0,
        asr_tune = 0,
        maghrib_tune = 0,
        sunset_tune = 0,
        isha_tune = 0,
        midnight_tune = 0,
        fajr_angle = "",
        maghrib_angle = "",
        isha_angle = "",
        shafaq = "general",
        iso8601 = False,
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
        if tune is True:
            self._tune = str(imsak_tune) + ',' + str(fajr_tune) + ',' \
                + str(sunrise_tune) + ',' + str(dhuhr_tune) + ',' \
                + str(asr_tune) + ',' + str(maghrib_tune) + ',' \
                + str(sunset_tune) + ',' + str(isha_tune) + ',' \
                + str(midnight_tune)
        else:
            self._tune = False

        if self._calculation_method == 99:
            self.custom_method(fajr_angle, maghrib_angle, isha_angle)
        else: self._method_settings = False

        date_parsed = datetime.strptime(date, "%Y-%m-%d")
        self._date = date_parsed.strftime("%d-%m-%Y")
        self.iso8601 = 'true' if iso8601 else 'false'

    def custom_method(self, fajr_angle, maghrib_angle, isha_angle):
            if fajr_angle is None: fajr_angle = "null"
            if maghrib_angle is None: maghrib_angle = "null"
            if isha_angle is None: isha_angle = "null"
            self._method_settings = str(fajr_angle) + ',' + str(maghrib_angle) \
                + ',' +str(isha_angle)

    def fetch_prayer_times(self):
        """Return prayer times for defined parameters."""
        url = f"{self.API_URL}/{self._date}"
        params = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "method": self._calculation_method,
            "iso8601": self.iso8601,
        }
        if self._school:
            params.update({"school": self._school})
        if self._midnight_mode:
            params.update({"midnightMode": self._midnight_mode})
        if self._lat_adj_method:
            params.update({"latitudeAdjustmentMethod": self._lat_adj_method})
        if self._tune:
            params.update({"tune": self._tune})
        if self._method_settings:
            params.update({"methodSettings": self._method_settings})

        response = requests.get(url, params=params, timeout=10)

        if not response.status_code == 200:
            raise InvalidResponseError(f"\nUnable to retrive prayer times. Url: {url}")

        resp = response.json()["data"]["timings"]
        resp["date"] = response.json()["data"]["date"]

        return resp
