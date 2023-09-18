import math


class DegreesRadiansConverter:
    def convert_to_radians(self, degrees: int, minutes: int):
        converted_minutes = minutes * (1/60)
        sum_of_degrees = degrees + converted_minutes
        converted_to_radians = sum_of_degrees * (math.pi / 180)
        return converted_to_radians

    def convert_to_degrees(self, radians: float):
        converted_to_degrees = radians * (180 / math.pi)
        whole_degrees = int(converted_to_degrees)
        decimal_fraction = converted_to_degrees - whole_degrees
        minutes = decimal_fraction * 60
        return whole_degrees, minutes
