import coordinates_interpolation
import requests


class CoordinateElevationFetcher:
    def __init__(self, latitude_point_a, longitude_point_a, latitude_point_b, longitude_point_b, granularity_meters):
        self.latitude_point_a = latitude_point_a
        self.longitude_point_a = longitude_point_a
        self.latitude_point_b = latitude_point_b
        self.longitude_point_b = longitude_point_b
        self.granularity_meters = granularity_meters

    def interpolate_coordinates(self):
        new_instance = coordinates_interpolation.CoordinateInterpolation(self.latitude_point_a, self.longitude_point_a,
                                                                        self.latitude_point_b, self.longitude_point_b,
                                                                        self.granularity_meters)
        return new_instance.interpolate_coordinates()

    def get_elevation(self, locations):
        api_url = "https://api.open-elevation.com/api/v1/lookup"

        try:
            response = requests.post(api_url, json={"locations": locations})
            response.raise_for_status()
            data = response.json()

            elevations = [result["elevation"] for result in data["results"]]
            return elevations
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None

    def get_elevation_data(self):
        locations_list = self.interpolate_coordinates()
        elevations = self.get_elevation(locations_list)

        elevation_data = [{"latitude": loc["latitude"], "longitude": loc["longitude"], "elevation": elev}
                          for loc, elev in zip(locations_list, elevations)]

        return elevation_data
