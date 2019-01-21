from .exceptions import *
import requests
from datetime import datetime


class PrayerTimesCalculator:
    CALCULATION_METHODS = {
        'shia': 0, 
        'karachi': 1,
        'isna': 2,
        'mwl': 3,
        'makkah': 4,
        'egas': 5,
        'igut': 6,
        'gulf': 7,
        'kuwait': 8,
        'qatar': 9,
        'muss': 10,
        'uoisdf': 11,
        'dibt': 12
    }

    API_URL = "http://api.aladhan.com/timings"

    def __init__(self, latitude: float, longitude: float,
                 calculation_method: str, date: str):
        self._latitude = latitude
        self._longitude = longitude

        calculation_method = calculation_method.lower()
        if calculation_method in self.CALCULATION_METHODS:
            self._calculation_method = self.CALCULATION_METHODS[
                calculation_method]
        else:
            raise CalculationMethodError("\nInvalid Calculation Method.  Must "
                                         "be one of: {}".format(
                ', '.join(self.CALCULATION_METHODS.keys())))

        date_parsed = datetime.strptime(date, '%Y-%m-%d')
        self._timestamp = int(date_parsed.timestamp())

    def fetch_prayer_times(self):
        url = "{}/{}?latitude={}&longitude={}&method={}".format(
            self.API_URL, self._timestamp, self._latitude, self._longitude,
            self._calculation_method)

        response = requests.get(url)

        if not response.status_code == 200:
            raise InvalidResponseError(
                "\nUnable to retrive prayer times.  Url: {}".format(url))

        return response.json()['data']['timings']
