import coordinates_interpolation
import requests


class CoordinateElevationFetcher:
    """
    A class to represent a fetcher for elevations of coordinates.

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
    interpolate_coordinates():
        Interpolates the steps in between point a and b, returns the interpolated points.
    get_elevation():
        Takes all points, fetches and returns the elevation data.
    get_elevation_data():
        Takes in longitude, latitude and elevation for all points, returns complete dictionary.
    """

    def __init__(self, latitude_point_a: float, longitude_point_a: float, latitude_point_b: float, longitude_point_b: float, granularity_meters: float):
        """
        Constructs all the necessary attributes for the CoordinateElevationFetcher object.

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

    def interpolate_coordinates(self) -> dict:
        """
        Interpolates the steps in between point a and b, returns the interpolated points.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        The coordinates (longitude and latitude) of the orignal point a and b as well as those of the interpolated points in between in the form of a dictionary.
        """
        new_instance = coordinates_interpolation.CoordinateInterpolation(self.latitude_point_a, self.longitude_point_a,
                                                                         self.latitude_point_b, self.longitude_point_b,
                                                                         self.granularity_meters)
        return new_instance.interpolate_coordinates()

    def get_elevation(self, locations) -> list:
        """
        Takes all points, fetches and returns the elevation data.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        The elevation in meters of the orignal point a and b and the interpolated points in between in the form of a list.
        """
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

    def get_elevation_data(self) -> dict:
        """
        Takes the longitude and latitude of the points and adds the elevation.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        The complete dictionary of the coordinates (longitude & latitude) including their elevation in meters.
        """
        locations_list = self.interpolate_coordinates()
        elevations = self.get_elevation(locations_list)

        elevation_data = [{"latitude": loc["latitude"], "longitude": loc["longitude"], "elevation": elev}
                          for loc, elev in zip(locations_list, elevations)]

        return elevation_data
