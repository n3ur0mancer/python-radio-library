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

        plt.figure(facecolor="#000000")
        ax = plt.axes()
        ax.set_facecolor("#000000")

        plt.fill_between(latitudes, elevations, color='#FFA500', alpha=0.15)

        plt.grid(True, linestyle='dashed', linewidth=0.5, color='gray')

        spines = plt.gca().spines
        for spine in spines.values():
            spine.set_visible(True)
            spine.set_color('white')
            spine.set_linestyle('-')

        plt.plot(latitudes, elevations, color='#FFA500', linewidth=0.5, clip_on=True, label='Elevation')

        plt.title('Elevation along Latitude', color='white', loc='left', font="Roboto", fontsize=15)
        plt.xlabel('Latitude', color='white', font="Roboto")
        plt.xticks(color='white', font="Roboto")
        plt.ylabel('Elevation (meters)', color='white', font="Roboto")
        plt.yticks(color='white', font="Roboto")

        plt.legend(facecolor="black", labelcolor="white", prop={'family': 'Roboto'})
        plt.xlim(min(latitudes), max(latitudes))
        plt.ylim((min(elevations)-(min(elevations)/100)), (max(elevations)+(max(elevations)/100)))

        plt.show()


new_plotter = ElevationProfilePlotter(47.502136, 9.235879, 47.711853, 9.647965, 100)
new_plotter.plot_elevation_profile()
