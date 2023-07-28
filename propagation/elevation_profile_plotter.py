import matplotlib.pyplot as plt
import coordinates_elevation_fetcher


class ElevationProfilePlotter:
    def __init__(self, latitude_point_a, longitude_point_a, latitude_point_b, longitude_point_b, granularity_meters):
        self.latitude_point_a = latitude_point_a
        self.longitude_point_a = longitude_point_a
        self.latitude_point_b = latitude_point_b
        self.longitude_point_b = longitude_point_b
        self.granularity_meters = granularity_meters

    def plot_elevation_profile(self):
        data_fetcher = coordinates_elevation_fetcher.CoordinateElevationFetcher(self.latitude_point_a, self.longitude_point_a, self.latitude_point_b, self.longitude_point_b, self.granularity_meters)
        elevation_data = data_fetcher.get_elevation_data()

        latitudes = [item['latitude'] for item in elevation_data]
        elevations = [item['elevation'] for item in elevation_data]

        # Create the area chart
        plt.fill_between(latitudes, elevations, color='skyblue')
        plt.plot(latitudes, elevations, color='blue', label='Elevation')
        plt.title('Elevation along Latitude')
        plt.xlabel('Latitude')
        plt.ylabel('Elevation (meters)')
        plt.legend()
        plt.grid(False)
        plt.show()


new_plotter = ElevationProfilePlotter(47.502136, 9.235879, 47.711853, 9.647965, 100)
new_plotter.plot_elevation_profile()
