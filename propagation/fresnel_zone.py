import math


class FresnelZone:
    def __init__(self, wavelength_meter, distance_meter):
        self.wavelength_meter = wavelength_meter
        self.distance_meter = distance_meter

    def calc_fresnel_zone(self):
        return ((math.sqrt(self.wavelength_meter * self.distance_meter)) / 2) * 0.6


input_wavelength_meter = float(input("Wavelength in meter: "))
input_distance_meter = float(input("Distance between stations in meter: "))

new_fresnel_zone = FresnelZone(input_wavelength_meter, input_distance_meter)
fresnel_result = new_fresnel_zone.calc_fresnel_zone()

print(f"The Fresnel Zone is: {round(fresnel_result, 2)} m")
