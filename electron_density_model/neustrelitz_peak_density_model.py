import math


class LocalTimeF1:
    def __init__(self, local_time_hours: int, latitude_radians: float, sun_declination_radians: float, day_of_year: int, coefficients: list):
        self.local_time_hours = local_time_hours
        self.latitude_radians = latitude_radians
        self.sun_declination_radians = sun_declination_radians
        self.day_of_year = day_of_year
        self.coefficients = coefficients

    # method calculates diurnal, semi-diurnal, and ter-diurnal harmonic components related to variations in local time
    def calculate_local_time_variations(self):
        phase_shift = 14
        variation_diurnal = (
            2 * math.pi * (self.local_time_hours - phase_shift)) / 24
        variation_semi_diurnal = (2 * math.pi * self.local_time_hours) / 12
        variation_ter_diurnal = (2 * math.pi * self.local_time_hours) / 8
        return variation_diurnal, variation_semi_diurnal, variation_ter_diurnal

    # method calculates various angles related to solar zenith angles based on geographic latitude and sun declination
    def calculate_solar_zenith_angles(self):
        PF1 = 0.4
        cos_solar_zenith_angle = (math.sin(self.latitude_radians) * math.sin(self.sun_declination_radians))+(
            math.cos(self.latitude_radians) * math.cos(self.sun_declination_radians))
        cos_adjusted_zenith_angle = math.cos(cos_solar_zenith_angle) - (
            ((2 * self.latitude_radians) / math.pi) * math.sin(self.sun_declination_radians))
        cos_further_adjusted_zenith_angle = math.cos(
            cos_solar_zenith_angle) + PF1
        return cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle

    # method models the summer daytime bite-out effect using several mathematical expressions involving latitude, day of the year, and other parameters
    def calculate_summer_daytime_bite_out(self):
        LTBO = 13 + 1.5 * math.cos((2 * math.pi * (self.day_of_year - 181)) / 365.25) * \
            (self.latitude_radians / math.fabs(self.latitude_radians))
        fixed_graographic_latitude = 45
        gaussian_half_width_degree = 14
        gaussian_half_width_hours = 3
        summer_daytime_bite_out = math.exp(-(((math.fabs(self.latitude_radians) - fixed_graographic_latitude**2)) / (
            2 * gaussian_half_width_degree**2))) * math.cos((2 * math.pi * (self.day_of_year - 181)) / 365.25) * math.exp(-((self.latitude_radians - LTBO)**2 / 2 * gaussian_half_width_hours**2)) * (self.latitude_radians / math.fabs(self.latitude_radians))
        return summer_daytime_bite_out

    # method integrates the results from the previous calculations to compute the local time variation factor F1
    def calculate_local_time_F1(self):
        variation_diurnal, variation_semi_diurnal, variation_ter_diurnal = self.calculate_local_time_variations()
        cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle = self.calculate_solar_zenith_angles()
        summer_daytime_bite_out = self.calculate_summer_daytime_bite_out()

        local_time_F1 = math.cos(cos_further_adjusted_zenith_angle) + (self.coefficients[0] * math.cos(variation_diurnal) + self.coefficients[1] * math.cos(variation_semi_diurnal) + self.coefficients[2] * math.sin(
            variation_semi_diurnal) + self.coefficients[3] * math.cos(variation_ter_diurnal) + self.coefficients[4] * math.sin(variation_ter_diurnal)) * math.cos(cos_adjusted_zenith_angle) + self.coefficients[5] * summer_daytime_bite_out
        return local_time_F1


class SeasonalVariationF2:
    def __init__(self, day_of_year: int, coefficients: list):
        self.day_of_year = day_of_year
        self.coefficients = coefficients

    # calculating the annual variation
    def calculate_annual_variation(self):
        phase_shift = 18
        annual_variation = (
            2 * math.pi * (self.day_of_year - phase_shift)) / 365.25
        return annual_variation

    # calculating the semi-annual variation
    def calculate_semi_annual_variation(self):
        phase_shift = 6
        semi_annual_variation = (
            4 * math.pi * (self.day_of_year - phase_shift)) / 365.25
        return semi_annual_variation

    # calculating the seasonal variation
    def calculate_seasonal_variation_F2(self):
        annual_variation = self.calculate_annual_variation()
        semi_annual_variation = self.calculate_semi_annual_variation()

        seasonal_variation_F2 = 1 + (self.coefficients[6] * math.cos(
            annual_variation)) + (self.coefficients[7] * math.cos(semi_annual_variation))
        return seasonal_variation_F2


class NeustrelitzPeakElectronModel:
    def __init__(self, local_time_F1: float, seasonal_variation_F2: float):
        self.local_time_F1 = local_time_F1
        self.seasonal_variation_F2 = seasonal_variation_F2


# Testing the classes
local_time_hours = 18
latitude_radians = 0.9730
sun_declination_radians = 0.8712
day_of_year = 258
coefficients = [1, 2, 3, 4, 5, 6, 7, 8]

test_F1 = LocalTimeF1(local_time_hours, latitude_radians,
                      sun_declination_radians, day_of_year, coefficients)
results_F1 = test_F1.calculate_local_time_F1()
print(results_F1)

test_F2 = SeasonalVariationF2(day_of_year, coefficients)
results_F2 = test_F2.calculate_seasonal_variation_F2()
print(results_F2)
