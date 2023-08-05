import math


class FresnelZone:
    """
    A class to represent the Fresnel Zone between two points.

    ...

    Attributes
    ----------
    wavelength_meter : float
        the size of the wavelength in meters
    distance_meter : float
        the distance bewtween the two points in meters

    Methods
    -------
    calc_fresnel_zone():
        Calculates the Fresnel Zone between two points.
    """

    def __init__(self, wavelength_meter, distance_meter):
        """
        Constructs all the necessary attributes for the FresnelZone object.

        Parameters
        ----------
            wavelength_meter : float
                the size of the wavelength in meters
            distance_meter : float
                the distance bewtween the two points in meters
        """
        self.wavelength_meter = wavelength_meter
        self.distance_meter = distance_meter

    def calc_fresnel_zone(self):
        """
        Calculates the Fresnel Zone.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        Returns the Fresnel Zone in meters as a float.
        """
        return ((math.sqrt(self.wavelength_meter * self.distance_meter)) / 2) * 0.6


input_wavelength_meter = float(input("Wavelength in meter: "))
input_distance_meter = float(input("Distance between stations in meter: "))

new_fresnel_zone = FresnelZone(input_wavelength_meter, input_distance_meter)
fresnel_result = new_fresnel_zone.calc_fresnel_zone()

print(f"The Fresnel Zone is: {round(fresnel_result, 2)} m")
