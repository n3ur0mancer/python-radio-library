import math


class NeustrelitzPeakElectronModel:
    def __init__(self, local_time_hours: int, latitude_radians: float, sun_declination_radians: float):
        self.local_time_hours = local_time_hours
        self.latitude_radians = latitude_radians
        self.sun_declination_radians = sun_declination_radians

    def local_time_variations(self, local_time_hours):
        phase_shift = 14
        variation_diurnal = (
            2 * math.pi * (local_time_hours - phase_shift)) / 24
        variation_semi_dirunal = (2 * math.pi * local_time_hours) / 12
        variation_ter_diurnal = (2 * math.pi * local_time_hours) / 8
        return variation_diurnal, variation_semi_dirunal, variation_ter_diurnal

    def solar_zenith_angle(self, latitude_radians, sun_declination_radians):
        PF1 = 0.4
        cos_solar_zenith_angle = (math.sin(latitude_radians) * math.sin(sun_declination_radians))+(
            math.cos(latitude_radians) * math.cos(sun_declination_radians))
        cos_adjusted_zenith_angle = math.cos(cos_solar_zenith_angle) - (
            ((2 * latitude_radians) / math.pi) * math.sin(sun_declination_radians))
        cos_further_adjusted_zenith_angle = math.cos(
            cos_solar_zenith_angle) + PF1
        return cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle
