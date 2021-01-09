"""
Functions for use in solar radiation calculations based on a datetime_object:
Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)

Attention: UTC time stamped measurements must be converted to local standard time.
Example:
    Assuming that the data form a Pandas Dataframe object with a date - time timestamp in UTC, the conversion is made
    as follows:

    pandas_dataframe.index = df.index + pd.Timedelta(hours=2)  # Converts timestamp from UTC to Greek local time

Modules:

declination: solar declination angle (rad)
equation_of_time: equation of time (minutes)
fractional_year: fractional year (rad)
hour_angle: solar hour angle (rad)
saz: solar azimuth angle (rad)
sza: solar zenith angle (rad)
true_solar_time: true solar time as python datetime object YYYY-MM-DD h:m:s

libraries used: numpy as np

Version 1.01 2020-01-08
Intro of numpy.radians() function

Version 1.02 2020-01-09
Change of some names

A. Argiriou, LAPUP, University of Patras
"""

import pandas as pd
import numpy as np


def declination(datetime_object):
    """
    Calculates the solar declination
    :param: datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :return: solar declination angle (rad)
    """

    return 0.006918 - 0.399912 * np.cos(fractional_year(datetime_object)) + 0.070257 * np.sin(fractional_year
                            (datetime_object)) - 0.006758 * np.cos(2 * fractional_year(datetime_object)) + 0.000907 * \
             np.sin(2 * fractional_year(datetime_object)) - 0.002697 * np.cos(3 * fractional_year(datetime_object)) +\
                                                                 0.00148 * np.sin(3 * fractional_year(datetime_object))


def equation_of_time(datetime_object):
    """
    Calculates the equation of time
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :return: equation of time (minutes)
    """

    return 229.18 * (0.000075 + 0.001868 * np.cos(fractional_year(datetime_object)) - 0.032077 * np.sin(fractional_year
            (datetime_object)) - 0.014615 * np.cos(2 * fractional_year(datetime_object)) - 0.040849 *
                     np.sin(2 * fractional_year(datetime_object)))


def fractional_year(datetime_object):
    """
    Calculates the fractional year corresponding to a datetime object
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :return: fractional year (radians)
    """
    return 2 * np.pi * (datetime_object.dayofyear - 1 + (datetime_object.hour - 12) / 24) / 365


def true_solar_time(datetime_object, longitude):
    """
    Calculates the true solar time (TST)
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :param longitude: longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :return: true solar time as python datetime object YYYY-MM-DD h:m:s
    """

    timezone = round(longitude / 15) + 1

    time_offset = equation_of_time(datetime_object) + 4. * longitude - 60. * timezone

    return datetime_object + pd.Timedelta(minutes=time_offset)


def hour_angle(datetime_object, longitude):
    """
    Calculates the solar hour angle
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :param longitude: longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :return: solar hour angle (rad)
    """

    tst = true_solar_time(datetime_object, longitude)
    tst_decimal = tst.hour + (tst.minute + (tst.second + tst.microsecond * 10 ** -6) / 60.) / 60.

    return np.radians(15. * (tst_decimal - 12.))


def sza(datetime_object, latitude, longitude):
    """
    Calculates the solar zenith angle
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :param longitude:longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :param latitude: latitude at the position of interest in degrees (positive to the north of the equator)
    :return: solar zenith angle (rad)
    """

    return np.arccos(np.sin(np.radians(latitude)) * np.sin(declination(datetime_object)) + np.cos(np.radians(latitude))
                     * np.cos(declination(datetime_object)) * np.cos(hour_angle(datetime_object, longitude)))


def saz(datetime_object, latitude, longitude):
    """
    Calculates the solar azimuth angle
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
    :param longitude:longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :param latitude: latitude at the position of interest in degrees (positive to the north of the equator)
    :return: solar azimuth angle (rad)
    """

    return 2 * np.pi - np.arccos((np.sin(declination(datetime_object)) * np.cos(np.radians(latitude)) -
                                  np.cos(hour_angle(datetime_object, longitude)) * np.cos(declination(datetime_object))
                                 * np.sin(np.radians(latitude))) / np.sin(sza(datetime_object, latitude, longitude)))

# Example of application on solar data from the LAPUP radiometric station in Patras


df = pd.read_csv('Solar_1min_2019.txt', usecols=[0, 6], index_col=0, parse_dates=True, sep=',', header=None)

df.index = df.index + pd.Timedelta(hours=2)  # Converts timestamp from UTC to local time

# Latitude and longitude in decimal form

lat = 38.29138889
lon = 21.78861111

for i in [680, 250000]:
    print(df.index[i])
    print(hour_angle(df.index[i], lon))
    print(90 - np.rad2deg(sza(df.index[i], lat, lon)))
    print(np.rad2deg(saz(df.index[i], lat, lon)))
