import matplotlib.pyplot as plt
import coordinates_elevation_fetcher

latitude_a = 47.515952
longitude_a = 10.230955
latitude_b = 47.301533
longitude_b = 10.786652
granularity_meters = 250

data_fetcher = coordinates_elevation_fetcher.CoordinateElevationFetcher(latitude_a, longitude_a, latitude_b, longitude_b, granularity_meters)
elevation_data = data_fetcher.get_elevation_data()

latitudes = [item['latitude'] for item in elevation_data]
elevations = [item['elevation'] for item in elevation_data]

# Create the area chart
plt.fill_between(latitudes, elevations, color='skyblue')
plt.plot(latitudes, elevations, color='blue', label='Elevation')
plt.xlabel('Latitude')
plt.ylabel('Elevation (meters)')
plt.title('Elevation along Latitude')
plt.legend()
plt.grid(False)
plt.show()
