from math import radians, cos, sin, asin, sqrt
import numpy as np


class CoordinateInterpolation:
    def __init__(self, latitude_point_a, longitude_point_a, latitude_point_b, longitude_point_b, granularity_meters):
        self.latitude_point_a = latitude_point_a
        self.longitude_point_a = longitude_point_a
        self.latitude_point_b = latitude_point_b
        self.longitude_point_b = longitude_point_b
        self.granularity_meters = granularity_meters

    def calculate_distance_km(self):
        longitude_a = radians(self.longitude_point_a)
        latitude_a = radians(self.latitude_point_a)
        longitude_b = radians(self.longitude_point_b)
        latitude_b = radians(self.latitude_point_b)

        distance_longitude = longitude_a - longitude_b
        distance_latitude = latitude_a - latitude_b

        haversine_half_angle = sin(distance_latitude / 2)**2 + cos(latitude_a) * cos(latitude_b) * sin(distance_longitude / 2)**2

        great_circle_angular_distance = 2 * asin(sqrt(haversine_half_angle))

        radius_earth = 6371

        distance_km_points = great_circle_angular_distance * radius_earth

        return distance_km_points

    def calculate_number_of_points(self):
        distance_km = self.calculate_distance_km() * 1000
        number_of_points = round(distance_km / self.granularity_meters)

        return number_of_points

    def interpolate_coordinates(self):
        number_of_points = self.calculate_number_of_points()

        t_values = np.linspace(0, 1, number_of_points)

        latitude_interpolated = self.latitude_point_a + t_values * (self.latitude_point_b - self.latitude_point_a)
        longitude_interpolated = self.longitude_point_a + t_values * (self.longitude_point_b - self.longitude_point_a)

        interpolated_coordinates = list(zip(latitude_interpolated, longitude_interpolated))

        return interpolated_coordinates


interpolator = CoordinateInterpolation(47.684282, 9.640046, 47.652013, 9.525812, 1000)

distance_km = interpolator.calculate_distance_km()
number_of_points = interpolator.calculate_number_of_points()
interpolated_coordinates = interpolator.interpolate_coordinates()

print(distance_km, number_of_points)
print(interpolated_coordinates)
