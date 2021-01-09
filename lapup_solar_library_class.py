"""
Class for solar radiation calculations based on a datetime_object:
Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)

Attention: UTC time stamped measurements must be converted to local standard time.
Example:
    Assuming that the data form a Pandas Dataframe object with a date - time timestamp in UTC, the conversion is made
    as follows:

    pandas_dataframe.index = df.index + pd.Timedelta(hours=2)  # Converts timestamp from UTC to Greek local time

Modules:

decl: solar declination angle (rad)
eqtime: equation of time (minutes)
fractional_year: fractional year (rad)
hour_angle: solar hour angle (rad)
sazimuth: solar azimuth angle (rad)
sza: solar zenith angle (rad)
true_solar_time: true solar time as python datetime object YYYY-MM-DD h:m:s

libraries used: numpy as np

Version 1.01
Intro of numpy.radians() function

A. Argiriou, LAPUP, University of Patras, 2020-01-08
"""

import pandas as pd
import numpy as np


class SolarGeometry:

    def __init__(self, datetime_object, latitude, longitude):
        self.datetime_object = datetime_object
        self.latitude = latitude
        self.longitude = longitude
        self.fractional_year = 2 * np.pi * (self.datetime_object.dayofyear - 1 + (self.datetime_object.hour - 12) / 24)\
                               / 365
        self.declination = 0.006918 - 0.399912 * np.cos(self.fractional_year) + 0.070257 * np.sin(self.fractional_year)\
                           - 0.006758 * np.cos(2 * self.fractional_year) + 0.000907 * np.sin(2 * self.fractional_year)\
                           - 0.002697 * np.cos(3 * self.fractional_year) + 0.00148 * np.sin(3 * self.fractional_year)
        self.equation_of_time = 229.18 * (0.000075 + 0.001868 * np.cos(self.fractional_year) - 0.032077 *
                                          np.sin(self.fractional_year) - 0.014615 * np.cos(2 * self.fractional_year) -
                                          0.040849 * np.sin(2 * self.fractional_year))
        
    # def fractional_year(self):
    #     return 2 * np.pi * (self.datetime_object.dayofyear - 1 + (self.datetime_object.hour - 12) / 24) / 365
    # 
    # def declination(self):
    #     return 0.006918 - 0.399912 * np.cos(self.fractional_year) + 0.070257 * np.sin(self.fractional_year) - 0.006758\
    #            * np.cos(2 * self.fractional_year) + 0.000907 * np.sin(2 * self.fractional_year) - 0.002697 * np.cos(3 *
    #             self.fractional_year) + 0.00148 * np.sin(3 * self.fractional_year)


# Example of application on solar data from the LAPUP radiometric station in Patras


df = pd.read_csv('Solar_1min_2019.txt', usecols=[0, 6], index_col=0, parse_dates=True, sep=',', header=None)

df.index = df.index + pd.Timedelta(hours=2)  # Converts timestamp from UTC to local time

# Latitude and longitude in decimal form

lat = 38.29138889
lon = 21.78861111

event1 = SolarGeometry(df.index[680], lat, lon)
event2 = SolarGeometry(df.index[250000], lat, lon)

print(event1.datetime_object)
print(event1.latitude)
print(event1.longitude)
print(event1.fractional_year)
print(event1.declination)
print(event1.equation_of_time)

print(event2.datetime_object)
print(event2.latitude)
print(event2.longitude)
print(event2.fractional_year)
print(event2.declination)
print(event2.equation_of_time)