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


class SolarGeometry:

    def __init__(self, datetime_object, latitude, longitude):
        self.datetime_object = datetime_object
        self.latitude = latitude
        self.longitude = longitude

    def fractional_year(self):
        """
        Calculates the fractional year corresponding to a datetime object
        :param self: Date and time YYYY-MM-DD h:m:s (local standard time without the daylight savings shift)
        :return: fractional year (radians)
        """
        return 2 * np.pi * (self.dayofyear - 1 + (self.hour - 12) / 24) / 365



