# Prayer Times Calculator

Just a python package around [https://aladhan.com's](https://aladhan.com/prayer-times-api) API. Only tested on python3.

## Usage

```python
from prayer_times_calculator import PrayerTimesCalculator

# required parameters
lat = 41.881832
long = -87.623177
calc_method = 'isna'
date = "2018-11-27"
# optional parameters
school = "shafi"
midnightMode = "jafari"
latitudeAdjustmentMethod = "one seventh"

calc = PrayerTimesCalculator(
    latitude=lat,
    longitude=long,
    calculation_method=calc_method,
    date=date,
    school=school,
    midnightMode=midnightMode,
    latitudeAdjustmentMethod=latitudeAdjustmentMethod
)

times = calc.fetch_prayer_times()
```

the `fetch_prayer_times` method will return a dict similar to:

```python
{'Fajr': '05:31', 'Sunrise': '06:53', 'Dhuhr': '11:38', 'Asr': '14:03', 'Sunset': '16:22', 'Maghrib': '16:22', 'Isha': '17:44', 'Imsak': '05:21', 'Midnight': '23:38'}
```
