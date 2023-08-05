# Python Radio Library
 An assortment of radio related Python snippets.

## What's included? 

The `propagation` package currently holds the majority of the modules.

---

### Calculating the Fresnel Zone

To calculate the Fresnel zone, use the `fresnel_zone.py` module and it's included `FresnelZone` class. 

It takes the following parameters: 

| Parameter        | Description                                               |
|------------------|-----------------------------------------------------------|
| wavelength_meter | Wavelength of the signal in meters                        |
| distance_meter   | Distance between the transmitter and receiver (in meters) |

---

### Calculating the Knife Edge Diffraction 

To calculate the Fresnel zone, use the `knife_edge_diffraction.py` module and it's included `KnifeEdgeDiffraction` class. 

It takes the following parameters: 

| Parameter                        | Description                                                      |
|----------------------------------|------------------------------------------------------------------|
| distance_receiver_obstruction    | Distance between the receiver and the obstruction (in meters)    |
| distance_transmitter_obstruction | Distance between the transmitter and the obstruction (in meters) |
| height_obstruction               | Height of the obstruction (in meters)                            |
| wavelength_meter                 | Wavelength of the signal (in meters)      |

---

### Visualizing the line of sight between two points

![elevation_profile](https://github.com/n3ur0mancer/python-radio-library/assets/46748400/d218544e-aab2-4ef7-beeb-072653690305)

You can visualize the elevation profile between two points using their latitude & longitude coordinates.

Currently, you can use the `elevation_profile_plotter.py` module and the included `ElevationProfilePlotter` class to create a plot of the elevation profile. 

It takes the following parameters: 

| Parameter          | Description                                               |
|--------------------|-----------------------------------------------------------|
| latitude_point_a   | Latitude of point A (ex. 47.502136)                       |
| longitude_point_a  | Longitude of point A (ex. 9.235879)                       |
| latitude_point_b   | Latitude of point B                                       |
| longitude_point_b  | Longitude of point B                                      |
| granularity_meters | The distance between intermediate data points (in meters). Ddefault value of 100 m. |

How it works: 
1. The distance and amount of intermediate steps between the two points are calculated in the `coordinates_interpolation.py` module.
2. The coordinates of the intermediate steps are being interpolated in the same `coordinates_interpolation.py` module.
3. The elevation data for all the coordinates are being fetched from the API of https://open-elevation.com/ in the `coordinates_elevation_fetcher.py` module.
4. The elevation is being plotted with Matplotlib Pyplot in the `elevation_profile_plotter.py` module.

---

