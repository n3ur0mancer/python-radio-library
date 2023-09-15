import math


class LocalTimeF1:
    def __init__(self, local_time_hours: int, latitude_radians: float, sun_declination_radians: float):
        self.local_time_hours = local_time_hours
        self.latitude_radians = latitude_radians
        self.sun_declination_radians = sun_declination_radians

    def calculate_local_time_variations(self, local_time_hours):
        phase_shift = 14
        variation_diurnal = (
            2 * math.pi * (local_time_hours - phase_shift)) / 24
        variation_semi_diurnal = (2 * math.pi * local_time_hours) / 12
        variation_ter_diurnal = (2 * math.pi * local_time_hours) / 8
        return variation_diurnal, variation_semi_diurnal, variation_ter_diurnal

    def calculate_solar_zenith_angles(self, latitude_radians, sun_declination_radians):
        PF1 = 0.4
        cos_solar_zenith_angle = (math.sin(latitude_radians) * math.sin(sun_declination_radians))+(
            math.cos(latitude_radians) * math.cos(sun_declination_radians))
        cos_adjusted_zenith_angle = math.cos(cos_solar_zenith_angle) - (
            ((2 * latitude_radians) / math.pi) * math.sin(sun_declination_radians))
        cos_further_adjusted_zenith_angle = math.cos(
            cos_solar_zenith_angle) + PF1
        return cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle

    def calculate_summer_daytime_bite_out(self, latitude_radians, day_of_year):
        LTBO = 13 + 1.5 * math.cos((2 * math.pi * (day_of_year - 181)) / 365.25) * \
            (latitude_radians / math.fabs(latitude_radians))
        fixed_graographic_latitude = 45
        gaussian_half_width_degree = 14
        gaussian_half_width_hours = 3
        summer_daytime_bite_out = math.exp(-(((math.fabs(latitude_radians) - fixed_graographic_latitude**2)) / (
            2 * gaussian_half_width_degree**2))) * math.cos((2 * math.pi * (day_of_year - 181)) / 365.25) * math.exp(-((latitude_radians - LTBO)**2 / 2 * gaussian_half_width_hours**2)) * (latitude_radians / math.fabs(latitude_radians))
        return summer_daytime_bite_out

    def calculate_local_time_F1(self, variation_diurnal, variation_semi_diurnal, variation_ter_diurnal, cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle, summer_daytime_bite_out, coefficients):
        local_time_F1 = math.cos(cos_further_adjusted_zenith_angle) + (coefficients[0] * math.cos(variation_diurnal) + coefficients[1] * math.cos(variation_semi_diurnal) + coefficients[2] * math.sin(
            variation_semi_diurnal) + coefficients[3] * math.cos(variation_ter_diurnal) + coefficients[4] * math.sin(variation_ter_diurnal)) * math.cos(cos_adjusted_zenith_angle) + coefficients[5] * summer_daytime_bite_out
        return local_time_F1


test_F1 = LocalTimeF1()
results_F1 = test_F1.calculate_local_time_F1()


class NeustrelitzPeakElectronModel:
    def __init__(self, local_time_F1: float):
        self.local_time_F1 = local_time_F1
