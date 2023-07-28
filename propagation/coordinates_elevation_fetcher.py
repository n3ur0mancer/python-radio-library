import coordinate_interpolation
import requests

latitude_a = 47.684282
longitude_a = 9.640046
latitude_b = 47.652013
longitude_b = 9.525812
granularity_meters = 250

new_instance = coordinate_interpolation.CoordinateInterpolation(latitude_a, longitude_a, latitude_b, longitude_b, granularity_meters)
locations_list = new_instance.interpolate_coordinates()


def get_elevation(locations):
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


elevations = get_elevation(locations_list)

for location in range(len(locations_list)):
    locations_list[location]["elevation"] = elevations[location]

for location in locations_list:
    print(location)
