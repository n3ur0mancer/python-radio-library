import math


class KnifeEdgeDiffraction:
    def __init__(self, distance_receiver_obstruction, distance_transmitter_obstruction, height_obstruction, wavelength_meter):
        self.distance_receiver_obstruction = distance_receiver_obstruction
        self.distance_transmitter_obstruction = distance_transmitter_obstruction
        self.height_obstruction = height_obstruction
        self.wavelength_meter = wavelength_meter

    def calc_knife_edge_diffraction(self):
        fresnel_diffraction_parameter = self.height_obstruction * (
            math.sqrt((2 * (self.distance_transmitter_obstruction + self.distance_receiver_obstruction))
                      / (self.wavelength_meter * self.distance_transmitter_obstruction * self.distance_receiver_obstruction))
        )
        return fresnel_diffraction_parameter


test = KnifeEdgeDiffraction(1000, 1000, -20, 0.7)
print(test.calc_knife_edge_diffraction())
