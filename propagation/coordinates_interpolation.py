from math import radians, cos, sin, asin, sqrt
import numpy as np


class CoordinateInterpolation:
    """
    A class to represent the coordinate interpolation process.

    ...

    Attributes
    ----------
    latitude_point_a : float
        latitude of point a
    longitude_point_a : float
        longitude of point a
    latitude_point_b : float
        latitude of point b
    longitude_point_b : float
        longitude of point b
    granularity_meters : float
        distance between steps in meters

    Methods
    -------
    calculate_distance_km():
        calculates the distance between two points in km
    calculate_number_of_points():
        calculates the amount of intermediate points
    interpolate_coordinates():
        interpolates the coordinates of the intermediate points
    """

    def __init__(self, latitude_point_a, longitude_point_a, latitude_point_b, longitude_point_b, granularity_meters):
        """
        Constructs all the necessary attributes for the CoordinateInterpolation object.

        Parameters
        ----------
            latitude_point_a : float
                latitude of point a
            longitude_point_a : float
                longitude of point a
            latitude_point_b : float
                latitude of point b
            longitude_point_b : float
                longitude of point b
            granularity_meters : float
                distance between steps in meters
        """
        self.latitude_point_a = latitude_point_a
        self.longitude_point_a = longitude_point_a
        self.latitude_point_b = latitude_point_b
        self.longitude_point_b = longitude_point_b
        self.granularity_meters = granularity_meters

    def calculate_distance_km(self):
        """
        Calculates the distance in km between two given points.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        The distance between the two points in km in form of a float.
        """
        longitude_a = radians(self.longitude_point_a)
        latitude_a = radians(self.latitude_point_a)
        longitude_b = radians(self.longitude_point_b)
        latitude_b = radians(self.latitude_point_b)

        distance_longitude = longitude_a - longitude_b
        distance_latitude = latitude_a - latitude_b

        haversine_half_angle = sin(distance_latitude / 2)**2 + cos(
            latitude_a) * cos(latitude_b) * sin(distance_longitude / 2)**2

        great_circle_angular_distance = 2 * asin(sqrt(haversine_half_angle))

        radius_earth = 6371

        distance_km_points = great_circle_angular_distance * radius_earth

        return distance_km_points

    def calculate_number_of_points(self):
        """
        Calculates the amount of intermediate points.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        The amount of intermediate the two points as a rounded int.
        """
        distance_km = self.calculate_distance_km() * 1000
        number_of_points = round(distance_km / self.granularity_meters)

        return number_of_points

    def interpolate_coordinates(self):
        """
        Interpolates the coordinates of the intermediate points.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        The coordinates (longitude & latitude) of all the points in form of a dictionary.
        """
        number_of_points = self.calculate_number_of_points()

        t_values = np.linspace(0, 1, number_of_points)

        latitude_interpolated = self.latitude_point_a + t_values * \
            (self.latitude_point_b - self.latitude_point_a)
        longitude_interpolated = self.longitude_point_a + t_values * \
            (self.longitude_point_b - self.longitude_point_a)

        interpolated_coordinates = [{"latitude": lat, "longitude": lon} for lat, lon in zip(
            latitude_interpolated, longitude_interpolated)]

        return interpolated_coordinates
