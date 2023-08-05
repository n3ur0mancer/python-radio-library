import math


class KnifeEdgeDiffraction:
    """
    A class to represent the Knife Edge Diffraction.

    ...

    Attributes
    ----------
    distance_receiver_obstruction : int
        distance between the receiver and the obstruction
    distance_transmitter_obstruction : int
        distance between the transmitter and the obstruction
    height_obstruction : int
        height of the obstruction
    wavelength_meter : int
        size of the wavelength in meter

    Methods
    -------
    calc_knife_edge_diffraction():
        Calculates the Knife Edge Diffraction.
    """

    def __init__(self, distance_receiver_obstruction, distance_transmitter_obstruction, height_obstruction, wavelength_meter):
        """
        Constructs all the necessary attributes for the KnifeEdgeDiffraction object.

        Parameters
        ----------
            distance_receiver_obstruction : int
                distance between the receiver and the obstruction
            distance_transmitter_obstruction : int
                distance between the transmitter and the obstruction
            height_obstruction : int
                height of the obstruction
            wavelength_meter : int
                size of the wavelength in meter
        """
        self.distance_receiver_obstruction = distance_receiver_obstruction
        self.distance_transmitter_obstruction = distance_transmitter_obstruction
        self.height_obstruction = height_obstruction
        self.wavelength_meter = wavelength_meter

    def calc_knife_edge_diffraction(self):
        """
        Calculates the Knife edge diffraction.

        Parameters
        ----------
        Does not take additional arguments.

        Returns
        -------
        Returns the Fresnel Diffraction Parameter as a float.
        """
        fresnel_diffraction_parameter = self.height_obstruction * (
            math.sqrt((2 * (self.distance_transmitter_obstruction + self.distance_receiver_obstruction))
                      / (self.wavelength_meter * self.distance_transmitter_obstruction * self.distance_receiver_obstruction))
        )
        return fresnel_diffraction_parameter


test = KnifeEdgeDiffraction(1000, 1000, 20, 0.7)
print(test.calc_knife_edge_diffraction())
