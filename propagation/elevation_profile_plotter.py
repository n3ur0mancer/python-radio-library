import matplotlib.pyplot as plt
import coordinates_elevation_fetcher

latitude_a = 49.562072
longitude_a = 5.863934
latitude_b = 49.543993
longitude_b = 5.830670
granularity_meters = 50

data_fetcher = coordinates_elevation_fetcher.CoordinateElevationFetcher(latitude_a, longitude_a, latitude_b, longitude_b, granularity_meters)
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
