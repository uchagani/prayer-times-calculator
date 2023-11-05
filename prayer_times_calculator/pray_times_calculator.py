"""Prayer times calculator api."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Final

import requests

from .exceptions import CalculationMethodError, InvalidResponseError

API_URL: Final = "http://api.aladhan.com/v1/timings"

CALCULATION_METHODS: Final = {
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

SCHOOLS: Final = {"shafi": 0, "hanafi": 1}
MIDNIGHT_MODES: Final = {"standard": 0, "jafari": 1}
LAT_ADJ_METHODS: Final = {"middle of the night": 1, "one seventh": 2, "angle based": 3}


class PrayerTimesCalculator:
    """Prayer time calculator class."""

    def __init__(
        self,
        latitude: float,
        longitude: float,
        calculation_method: str,
        date: str,
        school: str = "",
        midnightMode: str = "",
        latitudeAdjustmentMethod: str = "",
        tune=False,
        imsak_tune=0,
        fajr_tune=0,
        sunrise_tune=0,
        dhuhr_tune=0,
        asr_tune=0,
        maghrib_tune=0,
        sunset_tune=0,
        isha_tune=0,
        midnight_tune=0,
        fajr_angle: float | int | None = None,
        maghrib_angle: float | int | None = None,
        isha_angle: float | int | None = None,
        shafaq="general",
        iso8601=False,
    ) -> None:
        if calculation_method.lower() not in CALCULATION_METHODS:
            raise CalculationMethodError(calculation_method, list(CALCULATION_METHODS))

        if school and school.lower() not in SCHOOLS:
            raise CalculationMethodError(school, list(SCHOOLS))

        if midnightMode and midnightMode.lower() not in MIDNIGHT_MODES:
            raise CalculationMethodError(midnightMode, list(MIDNIGHT_MODES))

        if (
            latitudeAdjustmentMethod
            and latitudeAdjustmentMethod.lower() not in LAT_ADJ_METHODS
        ):
            raise CalculationMethodError(
                latitudeAdjustmentMethod, list(LAT_ADJ_METHODS)
            )

        self._latitude = latitude
        self._longitude = longitude

        self._calculation_method = CALCULATION_METHODS[calculation_method.lower()]
        self._method_settings: str | None = None
        if self._calculation_method == 99:
            self._method_settings = self.parse_method_settings(
                fajr_angle, maghrib_angle, isha_angle
            )

        self._school = SCHOOLS.get(school.lower())
        self._midnight_mode = MIDNIGHT_MODES.get(midnightMode.lower())
        self._lat_adj_method = LAT_ADJ_METHODS.get(latitudeAdjustmentMethod.lower())

        if tune is True:
            tunes = [
                imsak_tune,
                fajr_tune,
                sunrise_tune,
                dhuhr_tune,
                asr_tune,
                maghrib_tune,
                sunset_tune,
                isha_tune,
                midnight_tune,
            ]
            self._tune = ",".join(map(str, tunes))
        else:
            self._tune = ""

        try:
            date_parsed = datetime.strptime(date, "%Y-%m-%d")
        except ValueError as err:
            raise ValueError("Invalid date string. Must be 'yyyy-mm-dd'") from err

        self._date = date_parsed.strftime("%d-%m-%Y")

        self.iso8601 = "true" if iso8601 else "false"

    @staticmethod
    def parse_method_settings(
        fajr_angle: float | int | None,
        maghrib_angle: float | int | None,
        isha_angle: float | int | None,
    ) -> str:
        """Return method settings string format."""
        method_settings: list[str] = []
        if fajr_angle is None:
            method_settings.append("null")
        elif isinstance(fajr_angle, (int, float)):
            method_settings.append(str(fajr_angle))
        else:
            raise ValueError("angle must be float.")
        if maghrib_angle is None:
            method_settings.append("null")
        elif isinstance(maghrib_angle, (int, float)):
            method_settings.append(str(maghrib_angle))
        else:
            raise ValueError("angle must be float.")
        if isha_angle is None:
            method_settings.append("null")
        elif isinstance(isha_angle, (int, float)):
            method_settings.append(str(isha_angle))
        else:
            raise ValueError("angle must be float.")
        return ",".join(method_settings)

    def fetch_prayer_times(self) -> dict[str, Any]:
        """Return prayer times for defined parameters."""
        url = f"{API_URL}/{self._date}"
        params: dict[str, Any] = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "method": self._calculation_method,
            "iso8601": self.iso8601,
        }
        if self._school:
            params["school"] = self._school
        if self._midnight_mode:
            params["midnightMode"] = self._midnight_mode
        if self._lat_adj_method:
            params["latitudeAdjustmentMethod"] = self._lat_adj_method
        if self._tune:
            params["tune"] = self._tune
        if self._method_settings:
            params["methodSettings"] = self._method_settings

        response = requests.get(url, params=params, timeout=10)

        if not response.status_code == 200:
            raise InvalidResponseError(f"Unable to retrive prayer times. Url: {url}")

        resp: dict[str, Any] = response.json()["data"]["timings"]
        resp["date"] = response.json()["data"]["date"]

        return resp
