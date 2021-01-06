"""
Functions for use in solar radiation calculations.

Modules:

libraries
import numpy as np

A. Argiriou, LAPUP, Dec 2020
"""

import pandas as pd
import numpy as np


def decl(datetime_object):
    """
    Calculates the solar declination
    :param: datetime_object - Date and (local standard) time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :returns: solar declination angle (rad)
    """

    return 0.006918 - 0.399912 * np.cos(gamma(datetime_object)) + 0.070257 * np.sin(gamma(datetime_object)) - 0.006758 \
           * np.cos(2 * gamma(datetime_object)) + 0.000907 * np.sin(2 * gamma(datetime_object)) - 0.002697 * \
           np.cos(3 * gamma(datetime_object)) + 0.00148 * np.sin(3 * gamma(datetime_object))


def eqtime(datetime_object):
    """
    Calculates the equation of time
    :param datetime_object: Date and (local standard) time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :returns: equation of time (eqtime) (minutes)
    """

    return 229.18 * (0.000075 + 0.001868 * np.cos(gamma(datetime_object)) - 0.032077 * np.sin(gamma(datetime_object))
                     - 0.014615 * np.cos(2 * gamma(datetime_object)) - 0.040849 * np.sin(2 * gamma(datetime_object)))


def gamma(datetime_object):
    """
    Calculates the fractional year corresponding to a datetime object
    :param datetime_object: Date and (local standard) time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :return: fractional year (in radians)
    """
    return 2 * np.pi * (datetime_object.dayofyear - 1 + (datetime_object.hour - 12) / 24) / 365


def true_solar_time(datetime_object, longitude):
    """
    Calculates the true solar time (TST)
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :param longitude: longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :return: true solar time as python datetime object YYYY-MM-DD h:m:s
    """

    timezone = round(longitude / 15) + 1

    time_offset = eqtime(datetime_object) + 4. * longitude - 60. * timezone

    return datetime_object + pd.Timedelta(minutes=time_offset)


def hour_angle(datetime_object, longitude):
    """
    Calculates the solar hour angle
    :param datetime_object: Date and time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :param longitude: longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :return: solar hour angle (deg)
    """

    tst = true_solar_time(datetime_object, longitude)
    tst_min = tst.hour * 60. + tst.minute + (tst.second + tst.microsecond * 10 ** -6) / 60.
    return tst_min / 4. - 180.


def cos_sza(datetime_object, longitude, latitude):
    """
    Calculates the cosine of the solar zenith angle
    :param datetime_object: datetime_object: Date and time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :param longitude:longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :param latitude: latitude at the position of interest in degrees (positive to the north of the equator)
    :return: the cosine of the solar zenith angle
    """

    return np.sin(latitude * np.pi / 180.) * np.sin(decl(datetime_object)) + np.cos(latitude * np.pi / 180.) * \
           np.cos(decl(datetime_object)) * np.cos(hour_angle(datetime_object, longitude) * np.pi / 180.)


def sazimuth(datetime_object, longitude, latitude):
    """
    Calculates the solar azimuth angle
    :param datetime_object: datetime_object: Date and time YYYY-MM-DD h:m:s (without the daylight savings shift)
    :param longitude:longitude at the position of interest in degrees (positive to the east of the Prime Meridian)
    :param latitude: latitude at the position of interest in degrees (positive to the north of the equator)
    :return: solar azimuth angle (rad)
    """
    if hour_angle(datetime_object, longitude) >= 0:
        sign = 1
    else:
        sign = -1

    return sign * np.abs(np.arccos(np.sin(latitude * np.pi / 180.) * cos_sza(datetime_object, longitude, latitude) -
                                   np.sin(decl(datetime_object))) / np.cos(latitude * np.pi / 180.) /
                         np.sin(np.arccos(cos_sza(datetime_object, longitude, latitude))))


df = pd.read_csv('Solar_1min_2019.txt', usecols=[0, 6], index_col=0, parse_dates=True, sep=',', header=None)

df.index = df.index + pd.Timedelta(hours=2)  # Converts timestamp from UTC to local time

lat = 38.29138889
lon = 21.78861111

#  my_time = df.index[680]
#  my_solar_time = true_solar_time(my_time, longitude)

for i in range(620, 689):
    print(df.index[i])
    print(sazimuth(df.index[i], lon, lat)*180/np.pi)
