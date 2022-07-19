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
# If tune = True, then you can tune the timings by adding the tune parameter
# (denoting addition / substraction in minutes)
# Please NOTE that tuning one prayer will not change another.
# So adding 3 mins to Maghrib will NOT automatically add 3 mins to Isha
tune = False
imsak_tune = 0
fajr_tune = 0
sunrise_tune = 0
dhuhr_tune = 0
asr_tune = 0
maghrib_tune = 0
sunset_tune = 0
isha_tune = 0
midnight_tune = 0
# If calc_method="custom", then you can override some of these variables
fajr_angle = 15
maghrib_angle = None
isha_angle = 15

calc = PrayerTimesCalculator(
    latitude=lat,
    longitude=long,
    calculation_method=calc_method,
    date=date,
    school=school,
    midnightMode=midnightMode,
    latitudeAdjustmentMethod=latitudeAdjustmentMethod,
    tune=tune,
    imsak_tune=imsak_tune,
    fajr_tune=fajr_tune,
    sunrise_tune=sunrise_tune,
    dhuhr_tune=dhuhr_tune,
    asr_tune=asr_tune,
    maghrib_tune=maghrib_tune,
    sunset_tune=sunset_tune,
    isha_tune=isha_tune,
    fajr_angle=fajr_angle,
    maghrib_angle=maghrib_angle,
    isha_angle=isha_angle,
)

times = calc.fetch_prayer_times()
```

the `fetch_prayer_times` method will return a dict similar to:

```python
{'Fajr': '05:31',
 'Sunrise': '06:53',
 'Dhuhr': '11:38',
 'Asr': '14:03',
 'Sunset': '16:22',
 'Maghrib': '16:22',
 'Isha': '17:44',
 'Imsak': '05:21',
 'Midnight': '22:57',
 'date': {'readable': '26 Nov 2018',
  'timestamp': '1543276800',
  'hijri': {'date': '17-03-1440',
   'format': 'DD-MM-YYYY',
   'day': '17',
   'weekday': {'en': 'Al Athnayn', 'ar': 'الاثنين'},
   'month': {'number': 3, 'en': 'Rabīʿ al-awwal', 'ar': 'رَبيع الأوّل'},
   'year': '1440',
   'designation': {'abbreviated': 'AH', 'expanded': 'Anno Hegirae'},
   'holidays': []},
  'gregorian': {'date': '26-11-2018',
   'format': 'DD-MM-YYYY',
   'day': '26',
   'weekday': {'en': 'Monday'},
   'month': {'number': 11, 'en': 'November'},
   'year': '2018',
   'designation': {'abbreviated': 'AD', 'expanded': 'Anno Domini'}}}}
```
